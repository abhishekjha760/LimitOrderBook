from collections import deque

from pylimitbook.tk import Bid, Ask, Trade
from pylimitbook.tree import Tree
from builtins import input
from six.moves import cStringIO as StringIO

def parse_csv(columns, line):
    
    data = {}
    split = line.split(',')
    for idx, name in enumerate(columns):
        data[name] = split[idx]
    return data

class Book(object):
    def __init__(self):
        self.trades = deque(maxlen=100)  
        self.bids = Tree()
        self.asks = Tree()
        self.last_tk = None
        self.last_timestamp = 0

    def process_bid_ask(self, tk):
        
        tree = self.asks
        if tk.is_bid:
            tree = self.bids
 
        if tk.acty_typ == 3:
            tree.remove_order_by_id(tk.idn)
        elif tk.acty_typ == 4:
            tree.update_order(tk)
        else:
            tree.insert_tk(tk)

    def bid(self, csv):
        columns = ['Record_ind', 'segment', 'order_no', 'quote_tm', 'buysell', 'acty_typ', 'symbol', 'series', 'vol_disc', 'vol_orgnl', 'limit_prc', 'pri_trig', 'mkt_ord_flg', 'StLoss_I', 'Io_flag', 'Algo_Ind']
        data = parse_csv(columns, csv)
        bid = Bid(data)
        if bid.timestamp > self.last_timestamp:
            self.last_timestamp = bid.timestamp
        self.last_tk = bid
        self.process_bid_ask(bid)
        return bid

    def bid_split(self, symbol, idn, qty, pri, timestamp):
        data = {
            'timestamp': timestamp,
            'qty': qty,
            'pri': pri,
            'idn': idn
        }
        bid = Bid(data)
        if bid.timestamp > self.last_timestamp:
            self.last_timestamp = bid.timestamp
        self.last_tk = bid
        self.process_bid_ask(bid)
        return bid

    def ask(self, csv):
        columns = ['Record_ind', 'segment', 'order_no', 'quote_tm', 'buysell', 'acty_typ', 'symbol', 'series', 'vol_disc', 'vol_orgnl', 'limit_prc', 'pri_trig', 'mkt_ord_flg', 'StLoss_I', 'Io_flag', 'Algo_Ind']
        data = parse_csv(columns, csv)
        ask = Ask(data)
        if ask.timestamp > self.last_timestamp:
            self.last_timestamp = ask.timestamp
        self.last_tk = ask
        self.process_bid_ask(ask)
        return ask

    def ask_split(self, symbol, idn, qty, pri, timestamp):
        data = {
            'timestamp': timestamp,
            'qty': qty,
            'pri': pri,
            'idn': idn
        }
        ask = Ask(data)
        if ask.timestamp > self.last_timestamp:
            self.last_timestamp = ask.timestamp
        self.last_tk = ask
        self.process_bid_ask(ask)
        return ask

    def trade(self, csv):
        columns = ['Record_ind', 'segment', 'order_no', 'quote_tm', 'buysell', 'acty_typ', 'symbol', 'series', 'vol_disc', 'vol_orgnl', 'limit_prc', 'pri_trig', 'mkt_ord_flg', 'StLoss_I', 'Io_flag', 'Algo_Ind']
        data = parse_csv(columns, csv)
        data['order_no'] = 0
        trade = Trade(data)
        if trade.timestamp > self.last_timestamp:
            self.last_timestamp = trade.timestamp
        self.last_tk = trade
        self.trades.appendleft(trade)
        return trade

    def trade_split(self, symbol, qty, pri, timestamp):
        data = {
            'timestamp': timestamp,
            'qty': qty,
            'pri': pri,
            'idn': 0
        }
        trade = Trade(data)
        if trade.timestamp > self.last_timestamp:
            self.last_timestamp = trade.timestamp
        self.last_tk = trade
        self.trades.appendleft(trade)
        return trade

    def __str__(self):
        # Efficient string concat
        file_str = StringIO()
        file_str.write(" Bids \n")
        if self.bids != None and len(self.bids) > 0:
            for k, v in self.bids.pri_tree.items(reverse=True):
                file_str.write('%s' % v)
        file_str.write("\n Asks \n")
        if self.asks != None and len(self.asks) > 0:
            for k, v in self.asks.pri_tree.items():
                file_str.write('%s' % v)
        file_str.write("\nTrades \n")
        if self.trades != None and len(self.trades) > 0:
            num = 0
            for entry in self.trades:
                if num < 5:
                    file_str.write(str(entry.qty) + " @ " \
                                   + str(entry.pri / 100) \
                                   + " (" + str(entry.timestamp) + ")\n")
                    num += 1
                else:
                    break
        file_str.write("\n")
        return file_str.getvalue()
