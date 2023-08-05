# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod

from quantdigger.kernel.engine.event import OrderEvent, Event
from quantdigger.kernel.datastruct import Position, TradeSide, Direction
from quantdigger.util import engine_logger as logger

class Positions(object):
    """ 当前相同合约持仓集合(可能不同时间段下单)。

    :ivar total: 持仓总数。
    :ivar positions: 持仓集合。
    :vartype positions: set
    """
    def __init__(self):
        self.total = 0
        self.positions = set()

    def profit(self, new_price):
        """ 根据当前的价格计算盈亏。
        
           :param float new_price: 当前价格。
           :return: 盈亏数额。
           :rtype: float
        """
        profit = 0
        for pos in self.positions:
            profit += pos.transaction.profit(new_price)
        return profit

    def margin(self, new_price):
        """ 根据当前价格计算这笔交易的保证金。
        
           :param float new_price: 当前价格。
           :return: 保证金。
           :rtype: float
        """
        margin = 0
        for pos in self.positions:
            margin += pos.transaction.margin(new_price)
        return margin


class DealPosition(object):
    """ 开仓，平仓对
        
        :ivar open: 开仓价
        :vartype open: float
        :ivar close: 平仓价
        :vartype close: float
    """
    def __init__(self, buy_trans, sell_trans):
        self.open = buy_trans
        self.close = sell_trans

    def profit(self):
        """ 盈亏额  """
        direction = self.open.order.direction
        if direction == Direction.LONG:
            return (self.close.price - self.open.price) * self.open.quantity
        else:
            return (self.open.price - self.close.price) * self.open.quantity

    @property
    def quantity(self):
        """ 成交量 """
        return self.open.quantity

    @property
    def open_datetime(self):
        """ 开仓时间 """
        return self.open.datetime

    @property
    def open_price(self):
        """ 开仓价格 """
        return self.open.price

    @property
    def close_datetime(self):
        """ 平仓时间 """
        return self.close.datetime

    @property
    def close_price(self):
        """ 平仓价格 """
        return self.close.price

    @property
    def direction(self):
        """ 空头还是多头 """
        return self.open.order.direction


class Blotter(object):
    """
    订单管理。
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def update_signal(self, event):
        """
        处理策略函数产生的下单事件。
        """
        raise NotImplementedError("Should implement update_signal()")

    @abstractmethod
    def update_fill(self, event):
        """
        处理委托单成交事件。
        """
        raise NotImplementedError("Should implement update_fill()")


class SimpleBlotter(Blotter):
    """
    简单的订单管理系统，直接给 :class:`quantdigger.kernel.engine.exchange.Exchange`
    对象发订单，没有风控。
    """
    def __init__(self, timeseries, events_pool, initial_capital=5000.0):
        self._timeseries = timeseries
        self.events = events_pool
        self._open_orders = list()
        self._pre_settlement = 0     # 昨日结算价
        self._datetime = None # 当前时间
        self._init_captial = initial_capital

        # 用于分析策略性能数据
        self.all_orders = []
        self.initial_capital = initial_capital    # 初始权益

        self.current_positions = {}  # 当前持仓 dict of list, 包含细节。
        self.current_holdings = {}  # 当前的资金 dict

        self.all_holdings = []   # 所有时间点上的资金 list of dict
        self.deal_positions = []   # 开平仓对

    def _init_state(self):
        self.current_holdings = {
                'cash': self.initial_capital,
                'commission':  0.0,
                'history_profit':  0.0,
                'equity': self.initial_capital
        }
        self.all_holdings = [{
            'datetime': self._start_date,
            'cash': self.initial_capital,
            'commission':  0.0,
            'equity': self.initial_capital
        }]

    def update_bar(self, bars):
        """ 当前bar数据更新。 """ 
        self._bars = bars

    def update_datetime(self, dt):
        """
        在新的价格数据来的时候触发。
        """
        # 
        if self._datetime == None:
            self._start_date = dt
            self._init_state()
        self._datetime = dt
        self._update_status(dt)

    def _update_status(self, dt):
        """ 更新历史持仓，当前权益。"""
        # 更新持仓历史。
        dp = { }
        dp['datetime'] = dt
        dp.update(self.current_positions)

        # 更新资金历史。
        ## @todo  由持仓历史推断资金历史。
        dh = { }
        dh['datetime'] = dt
        dh['commission'] = self.current_holdings['commission']
        profit = 0
        margin = 0

        # 计算当前持仓历史盈亏。
        # 以close价格替代市场价格。
        is_stock = True  # 默认是股票回测
        for contract, pos_info in self.current_positions.iteritems():
            new_price = self._bars[contract].close
            profit += pos_info.profit(new_price)
            ## @todo 用昨日结算价计算保证金
            margin += pos_info.margin(new_price)
            if not contract.is_stock:
                is_stock =  False   # 

        # 当前权益 = 初始资金 - 佣金 + 历史持仓盈亏 + 当前持仓历史盈亏
        dh['equity'] = self._init_captial - self.current_holdings['commission'] + self.current_holdings['history_profit'] + profit
        dh['cash'] = dh['equity'] - margin 
        if dh['cash'] < 0:
            if not is_stock:
                # 如果是期货需要追加保证金
                ## @bug 如果同时交易期货和股票，就有问题。
                raise Exception('需要追加保证金!')

        self.current_holdings['cash'] = dh['cash']
        self.current_holdings['equity'] = dh['equity']
        self.all_holdings.append(dh)

    def update_signal(self, event):
        """
        处理策略函数产生的下单事件。
        """
        assert event.type == Event.SIGNAL
        valid_orders = []
        for order in event.orders:
            if self._valid_order(order):
                self.events.put(OrderEvent(order)) 
                valid_orders.append(order)
            else:
                assert(False and "无效合约")
        self._open_orders.extend(valid_orders)
        self.all_orders.extend(valid_orders)
        #print "Receive %d signals!" % len(event.orders)
        #self.generate_naive_order(event.orders)

    def update_fill(self, event):
        """
        处理委托单成交事件。
        """
        assert event.type == Event.FILL
        t_order = None
        for i, order in enumerate(self._open_orders):
            if order.id == event.transaction.id:
                t_order = self._open_orders.pop(i)
                break
        assert(t_order)
        self._update_positions(t_order, event.transaction)
        self._update_holdings(event.transaction)

    def _update_positions(self, order, trans):
        ## @todo 把复杂统计单独出来。
        """ 更新持仓 """
        p = self.current_positions.setdefault(trans.contract, Positions())
        new_pos = Position(order, trans)
        if trans.side == TradeSide.KAI:
            # 开仓
            p.positions.add(new_pos)
            if trans.direction == Direction.LONG:
                p.total += trans.quantity 
            else:
                p.total -= trans.quantity 
        elif trans.side == TradeSide.PING:
            # 平仓
            if trans.direction == Direction.LONG:
                p.total -= trans.quantity 
            else:
                p.total += trans.quantity 
            to_delete = set()
            left_vol = trans.quantity
            for position in reversed(list(p.positions)):
                self.deal_positions.append(DealPosition(position, new_pos))
                if position.quantity < left_vol:
                    # 还需从之前的仓位中平。
                    left_vol -= position.quantity
                    to_delete.add(position)

                elif position.quantity == left_vol:
                    left_vol -= position.quantity
                    to_delete.add(position)
                    break 

                else:
                    position.quantity -= left_vol
                    to_delete.add(position)
                    left_vol = 0
                    break
            p.positions -= to_delete
            assert(left_vol == 0)

    def _update_holdings(self, trans):
        """
        更新资金
        """
        trans_cost = self._bars[trans.contract].close
        # 每笔佣金，和数目无关！
        self.current_holdings['commission'] += trans.commission
        # 平仓，更新历史持仓盈亏。
        if trans.side == TradeSide.PING:
            self.current_holdings['history_profit'] += trans.profit(trans_cost)

    def _valid_order(self, order):
        """ 判断订单是否合法。 """ 
        if order.side == TradeSide.PING:
            try:
                pos = self.current_positions[order.contract]
                if order.direction == Direction.LONG:
                    ## @todo 自动改变合法仓位。
                    if pos.total > 0:
                        return True 
                elif order.direction == Direction.SHORT:
                    ## @todo 自动改变合法仓位。
                    if pos.total < 0:
                        return True 
            except KeyError:
                # 没有持有该合约
                logger.warn("不存在合约[%s]" % order.contract)
                return False
            return False
        elif order.side == TradeSide.KAI:
            if self.current_holdings['cash'] < 0:
                raise Exception('没有足够的资金开仓') 
        return True

