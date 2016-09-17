from decimal import Decimal
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
        #TODO initialise all possible data structures
        self.pusher = pusherclient.Pusher(self.key)
        self.pusher.connect()

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
                                   "quote": quote,
                                   "message_type": message})

    def live_trades(self, message, base=None, quote=None):
        """trade:
           id, amount, price, type, timestamp, buy_order_id, sell_order_id"""
        self.lastprice[base][quote] = Decimal(json.loads(message)[price])

    def order_book(self, message, base=None, quote=None):
        """data:
           bids, asks"""
        self.orderbook[base][quote] = json.loads(message)

    def diff_order_book(self, message, base=None, quote=None):
        """data:
           bids, asks"""
        self.diffmessage = json.loads(message)
        todo = """implement a dict that has the price as index, and the side
                  and size as attribute"""

    def live_orders(self, message, base=None, quote=None, messagetype=None):
        """order_created, order_changed, order_deleted:
           id, amount, price, order_type, datetime"""
        if messagetype = "order_created":
            self.openorders[base][quote]["price"][message["price"] = message
            #TODO append if already present, set list and append if not present
            self.openorders[base][quote]["id"][message["id"]] = message
        if messagetype = "order_changed":
            #TODO try except keyerror
        if messagetype = "order_deleted":
            #TODO try except keyerror
