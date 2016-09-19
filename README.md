# bitstamp-python-websocket-client
Client for the Bitstamp websocket written in Python

Bitstamp does not use regular websockets, but sends messages through Pusher.
Implementations of both Bitstamp and Pusher logic in Python do exist, but this
repository keeps the two separate.

## Usage
Firstly, instantiate a new Bitstamp object.
```python
import bitstamp
client = bitstamp.wsclient.BitstampWebsocketClient()
```

Secondly, subscribe to data sources.
```python
client.subscribe("live_trades", "btc", "eur")
#this will update client.lastprice["btc"]["eur"]
client.subscribe("order_book", "btc", "usd") #choose either this one, for accuracy
client.subscribe("diff_order_book", "btc", "usd") #or this one, for speed
#both will keep client.orderbook["btc"]["usd"] up to date
client.subscribe("live_orders", "eur", "usd")
#this will keep self.openorders["eur"]["usd"] up to date, and stores open orders
#by id and by price
```

To get the data from the client, access its attributes. There are no functions to
return the data from the instantiated object.

## Third party source code included
* The folder pusherclient was copied from Erik Kulyk (ekulyk), and is under the
MIT license. Changes to pusherclient made here will be or have been proposed to
the [original repository](https://github.com/ekulyk/PythonPusherClient), if they
could be useful outside this project.
