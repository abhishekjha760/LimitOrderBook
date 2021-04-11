from bintrees import FastRBTree

from pylimitbook.orderList import OrderList
from pylimitbook.order import Order

class Tree(object):
    def __init__(self):
        self.ptree = FastRBTree()
        self.vol = 0
        self.prmp = {}  
        self.order_map = {}  
        self.mip = None
        self.mxp = None

    def __len__(self):
        return len(self.order_map)

    def get_pri(self, pri):
        return self.prmp[pri]

    def get_order(self, id_num):
        return self.order_map[id_num]

    def create_pri(self, pri):
        new_list = OrderList()
        self.ptree.insert(pri, new_list)
        self.prmp[pri] = new_list
        if self.mxp == None or pri > self.mxp:
            self.mxp = pri
        if self.mip == None or pri < self.mip:
            self.mip = pri

    def remove_pri(self, pri):
        self.ptree.remove(pri)
        del self.prmp[pri]

        if self.mxp == pri:
            try:
                self.mxp = max(self.ptree)
            except ValueError:
                self.mxp = None
        if self.mip == pri:
            try:
                self.mip = min(self.ptree)
            except ValueError:
                self.mip = None

    def pri_exists(self, pri):
        return pri in self.prmp

    def order_exists(self, id_num):
        return id_num in self.order_map

    def insert_tick(self, tick):
        if tick.pri not in self.prmp:
            self.create_pri(tick.pri)
        order = Order(tick, self.prmp[tick.pri])
        self.prmp[order.pri].append_order(order)
        self.order_map[order.id_num] = order
        self.vol += order.qty

    def update_order(self, tick):
        order = self.order_map[tick.id_num]
        original_vol = order.qty
        if tick.pri != order.pri:
            order_list = self.prmp[order.pri]
            order_list.remove_order(order)
            if len(order_list) == 0:
                self.remove_pri(order.pri)
            self.insert_tick(tick)
            self.vol -= original_vol
        else:
            order.update_qty(tick.qty, tick.pri)
            self.vol += order.qty - original_vol

    def remove_order_by_id(self, id_num):
        order = self.order_map[id_num]
        self.vol -= order.qty
        order.order_list.remove_order(order)
        if len(order.order_list) == 0:
            self.remove_pri(order.pri)
        del self.order_map[id_num]

    def max(self):
        return self.mxp

    def min(self):
        return self.mip
