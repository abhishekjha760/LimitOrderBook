from pylimitbook.order import Order

class OrderList(object):
    def __init__(self):
        self.head_order = None
        self.tail_order = None
        self.length = 0
        self.volume = 0  
        self.last = None

    def __len__(self):
        return self.length

    def __iter__(self):
        self.last = self.head_order
        return self

    def next(self):
        if self.last == None:
            raise StopIteration
        else:
            return_val = self.last
            self.last = self.last.next_order
            return return_val

    __next__ = next 

    def append_order(self, order):
        
        if len(self) == 0:
            order.next_order = None
            order.prordr = None
            self.head_order = order
            self.tail_order = order
        else:
            order.prordr = self.tail_order
            order.next_order = None
            self.tail_order.next_order = order
            self.tail_order = order
        self.length += 1
        self.volume += order.qty

    def remove_order(self, order):
        self.volume -= order.qty
        self.length -= 1
        if len(self) == 0:
            return
        # Remove from list of orders
        next_order = order.next_order
        prordr = order.prordr
        if next_order != None and prordr != None:
            next_order.prordr = prordr
            prordr.next_order = next_order
        elif next_order != None:
            next_order.prordr = None
            self.head_order = next_order
        elif prordr != None:
            prordr.next_order = None
            self.tail_order = prordr

    def move_tail(self, order):
        if order.prordr != None:
            order.prordr.next_order = self.next_order
        else:
            # Update the head order
            self.head_order = order.next_order
        order.next_order.prordr = order.prordr
        # Set the previous tail order's next order to this order
        self.tail_order.next_order = order
        self.tail_order = order
        order.prordr = self.tail_order
        order.next_order = None

    def __str__(self):
        from six.moves import cStringIO as StringIO

        file_str = StringIO()
        for order in self:
            file_str.write("%s\n" % str(order))
        return file_str.getvalue()
