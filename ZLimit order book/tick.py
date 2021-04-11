class Tick(object):
    def __init__(self, data):
        self.timestamp = int(data['quote_tm'])
        self.qty = int(data['vol_orgnl'])
        self.pri = convert_pri(data['limit_prc'], True)
        self.idn = data['order_no']
        

def convert_pri(pri, use_float):
    if use_float:
        return float(pri)

class Trade(Tick):
    def __init__(self, data):
        super(Trade, self).__init__(data)

class Ask(Tick):
    def __init__(self, data):
        super(Ask, self).__init__(data)
        self.is_bid = False
        self.acty_typ = data['acty_typ']

class Bid(Tick):
    def __init__(self, data):
        super(Bid, self).__init__(data)
        self.is_bid = True
        self.acty_typ = data['acty_typ']
