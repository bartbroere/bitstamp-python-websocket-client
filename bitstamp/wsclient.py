#from decimal import Decimal
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
                                  "usd": None},
                          "eur": {"usd": None}}
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
                                   "messagetype": message},
                           decode_json=True)
        if stream == "diff_order_book":
            orderbook = json.loads(requests.get( #TODO base quote here
                                   "https://www.bitstamp.net/api/order_book/"))
            self.orderbook[base][quote] = orderbook

    def live_trades(self, message, base=None, quote=None, *args, **kwargs):
        """trade:
           id, amount, price, type, timestamp, buy_order_id, sell_order_id"""
        self.lastprice[base][quote] = str(message["price"])

    def order_book(self, message, base=None, quote=None, *args, **kwargs):
        """Users should subscribe to either order_book or diff_order_book.
           order_book is a bit more accurate, but diff_order_book is probably
           quicker.
           data:
           bids, asks"""
        self.orderbook[base][quote] = message

    def diff_order_book(self, message, base=None, quote=None, *args, **kwargs):
        """data:
           bids, asks"""
        self.diffmessage = message
        todo = """implement a dict that has the price as index, and the side
                  and size as attribute, and copy the logic from the example
                  at bitstamp.net/websocket"""

    def live_orders(self, message, base=None, quote=None, messagetype=None,
                    *args, **kwargs):
        """order_created, order_changed, order_deleted:
           id, amount, price, order_type, datetime"""
        message["price"] = str(message["price"])
        if messagetype == "order_created":
            if message["price"] not in self.openorders[base][quote]["price"]:
                self.openorders[base][quote]["price"][message["price"]] = []
            self.openorders[base][quote]["price"][message["price"]].append(
                                                                message)
            self.openorders[base][quote]["id"][message["id"]] = message
        if messagetype == "order_changed":
            self.openorders[base][quote]["id"][message["id"]] = message
            i = 0
            for order in self.openorders[base][quote]["price"][
                                         message["price"]]:
                if order["id"] == message["id"]:
                    self.openorders[base][quote]["price"][
                                    message["price"]][i] = message
                i += 1
            self.openorders[base][quote]["price"]
        if messagetype == "order_deleted":
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
