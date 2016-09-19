# bitstamp-python-websocket-client
Client for the Bitstamp websocket written in Python

Bitstamp does not use regular websockets, but sends messages through Pusher.
Implementations of both Bitstamp and Pusher logic in Python do exist, but this
repository keeps the two separate.

## Third party source code included
* The folder pusherclient was copied from Erik Kulyk (ekulyk), and is under the
MIT license. Changes to pusherclient made here will be or have been proposed to
the [original repository](https://github.com/ekulyk/PythonPusherClient), if they
could be useful outside this project.
