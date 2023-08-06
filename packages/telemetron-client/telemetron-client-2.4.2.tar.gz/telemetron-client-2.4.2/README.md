# README #

A Python client for Telemetron.

## Dependencies

    Python 2.6+


## How to use the client

### Sending a counter using _UDP_, to localhost:2013:


    from telemetronclient import TelemetronClient as Client
    client = Client(prefix="foo")  # UDP localhost:2013
    client.inc("mycounter", 1000)
    client.flush()


### Sending a counter using _TCP_, to _metrics.external.com:2014_:


    from telemetronclient import TelemetronClient as Client
    client = Client(
        host="metrics.external.com",
        port=2014
        socket_type=Client.TCP_SOCKET,
        prefix="bar")
    client.inc("mycounter", 1000)
    client.flush()


## How to run tests

    pylint --rcfile pylint.rc telemetronclient/
    pep8 telemetronclient/
    nosetests


## Deployment instructions

### Using package:

    python setup.py install


### Using pip:

    pip install telemetron-client
