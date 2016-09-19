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
return the data from the instantiated object. The attributes that could be accessed
are:
* lastprice
  ```python
{'eur': {'usd': {'price': {}, 'id': {}}},
 'btc': {'usd': 607.38,
         'eur': {'price': {}, 'id': {}}}}
  ```
* orderbook
  ```python
{'eur': {'usd': {'price': {}, 'id': {}}},
 'btc': {'usd': {'price': {}, 'id': {}},
         'eur': {'bids': [['542.57000000', '0.09375660'], ['542.56000000', '0.64376270'], ['542.55000000', '1.04019586'], ['542.43000000', '0.01429072'], ['542.40000000', '9.90000000'], ['542.00000000', '0.59001845'], ['541.92000000', '0.54879067'], ['541.85000000', '0.54010071'], ['541.31000000', '20.00000000'], ['541.28000000', '1.51017572'], ['541.26000000', '0.01432070'], ['541.06000000', '0.27646712'], ['540.99000000', '0.05999999'], ['540.68000000', '0.01433069'], ['540.54000000', '3.01230000'], ['540.09000000', '0.01435068'], ['540.00000000', '1.89310414'], ['539.96000000', '3.05143258'], ['539.91000000', '0.20000000'], ['539.84000000', '0.33000000']],
                'asks': [['545.41000000', '1.22027127'], ['545.42000000', '7.45199753'], ['545.50000000', '5.00000000'], ['545.96000000', '1.77000000'], ['545.97000000', '2.13058700'], ['545.98000000', '0.40000000'], ['545.99000000', '11.68681858'], ['546.05000000', '0.00940000'], ['546.10000000', '2.00000000'], ['546.63000000', '0.01427073'], ['546.67000000', '20.00000000'], ['546.70000000', '1.75590000'], ['547.04000000', '0.12500000'], ['547.21000000', '0.01426074'], ['547.44000000', '0.55088459'], ['547.45000000', '1.96054000'], ['547.80000000', '0.01424075'], ['548.00000000', '0.02000000'], ['548.08000000', '3.13810000'], ['548.15000000', '0.11107291']]}}}
  ```
* openorders
  ```python
  ```

Note that all data points are strings, so users can convert them to their own
favourite data type.


## Third party source code included
* The folder pusherclient was copied from Erik Kulyk (ekulyk), and is under the
MIT license. Changes to pusherclient made here will be or have been proposed to
the [original repository](https://github.com/ekulyk/PythonPusherClient), if they
could be useful outside this project. *Currently the changes to PythonPusherClient
are not yet merged to the main branch. Use
[my own fork](https://github.com/bartbroere/PythonPusherClient) to have the
compatible version of PythonPusherClient!*
