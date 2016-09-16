import sys #debug line
import pusherclient

class BitstampWebsocketClient(object):

    def __init__(self, *args, **kwargs):
        self.key = "de504dc5763aeef9ff52"
        self.channels = {}
        self.messages = {"live_trades": ["trade"],
                         "order_book": ["data"],
                         "diff_order_book": ["data"],
                         "live_orders": ["order_created",
                                         "order_changed",
                                         "order_deleted"]}
        for channel in self.messages.keys():
            self.channels[channel] = []
            for pair in ["btceur",
                         "eurusd"]:
                self.channels[channel + "_" + pair] = []
        self.pusher = pusherclient.Pusher(self.key)
        self.pusher.connect()
        self.received = [] #debug variable

    def subscribe(self, stream, base, quote):
        if base + quote != 'btcusd':
            fullstream = stream + "_" + base + quote
        else:
            fullstream = stream
        self.channels[fullstream].append(self.pusher.subscribe(fullstream))
        for event in self.channels[fullstream]:
            for message in self.messages[stream]:
                event.bind(message,
                           getattr(self, stream),
                           kwargs={"base": base,
                                   "quote": quote})

    def live_trades(self, message, base=None, quote=None):
        """trade:
           id, amount, price, type, timestamp, buy_order_id, sell_order_id"""
        sys.stdout(base + quote + ": " + message)

    def order_book(self, message, base=None, quote=None):
        """data:
           bids, asks"""
        sys.stdout(base + quote + ": " + message)

    def diff_order_book(self, message, base=None, quote=None):
        """data:
           bids, asks"""
        sys.stdout(base + quote + ": " + message)

    def live_orders(self, message, base=None, quote=None):
        """order_created, order_changed, order_deleted:
           id, amount, price, order_type, datetime"""
        sys.stdout(base + quote + ": " + message)
