class Order(object):
    def __init__(self, tick, ordrl):
        self.next_order = None
        self.prordr = None
        self.tick = tick
        self.ordrl = ordrl

    def next_order(self):
        return self.next_order

    def prordr(self):
        return self.prordr

    def update_qty(self, new_qty, ntymstmp):
        if new_qty > self.qty and self.ordrl.tail_order != self:
            self.ordrl.move_tail(self)
        self.ordrl.volume -= self.qty - new_qty
        self.tick.timestamp = ntymstmp
        self.tick.qty = new_qty

    @property
    def id_num(self):
        return self.tick.idn

    @property
    def qty(self):
        return self.tick.qty

    @property
    def price(self):
        return self.tick.pri

    @property
    def is_bid(self):
        return self.tick.is_bid

    def __str__(self):
        return "%s\t@\t%.4f" % (self.qty, self.price / float(100))
