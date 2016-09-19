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
        self.orderbook = {"btc": {"eur": None,
                                  "usd": None
                          "eur": {"usd": None}
        self.lastprice = self.orderbook
        self.openorders = self.orderbook
        for base in self.openorders.keys():
            for quote in self.openorders[base].keys():
                self.openorders[base][quote] = {"price": {},
                                                "id": {}}
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
        self.lastprice[base][quote] = Decimal(message[price])

    def order_book(self, message, base=None, quote=None):
        """data:
           bids, asks"""
        self.orderbook[base][quote] = message

    def diff_order_book(self, message, base=None, quote=None):
        """data:
           bids, asks"""
        self.diffmessage = message
        todo = """implement a dict that has the price as index, and the side
                  and size as attribute, and copy the logic from the example
                  at bitstamp.net/websocket"""

    def live_orders(self, message, base=None, quote=None, messagetype=None):
        """order_created, order_changed, order_deleted:
           id, amount, price, order_type, datetime"""
        if messagetype = "order_created":
            self.openorders[base][quote]["price"][message["price"]] = message
            if message["price"] in self.openorders[base][quote]["price"]::
                self.openorders[base][quote]["price"].append(message)
            else:
                self.openorders[base][quote]["price"] = [message]
            self.openorders[base][quote]["id"][message["id"]] = message
        if messagetype = "order_changed":
            #TODO try except keyerror
        if messagetype = "order_deleted":
            try: del self.openorders[base][quote]["id"][message["id"]]
            except KeyError: pass
            try:
                i = 0
                for order in self.openorders[base][quote]["price"][
                                             message["price"]]:
                    if order["id"] == message["id"]:
                        del self.openorders[base][quote]["price"][
                                             message["price"]][i]
                    i += 1
            except KeyError: pass
