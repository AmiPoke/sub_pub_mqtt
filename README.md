# sub_pub_mqtt

## Description

This small script connects to two different MQTT-Brokers.

It subscribes to one topic at the first Broker (brokersub).

The received messages will be forwarded to the second Broker (brokerpub).

All Parameters are stored in `config.ini`. An empty file will be generated of not existent.

At the Moment, only unencrypted Connections are supported.

## Example Configfile

```config
[brokersub]
    host = someting.mqtt.io
    port = 1883
    user = user
    password = jlksd879QDD
    topic = pv/opendtu/battery/SOC

[brokerpub]
    host = test.mosquitto.org
    port = 1883
    user = 
    password = 
    topic = YmFyCiAgICBzdGF0deTTzPSAiIgogI/CellMinMilliVolt
```
