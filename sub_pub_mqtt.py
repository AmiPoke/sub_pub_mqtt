#!/usr/bin/env python3

# Dieses Skript stellt Verbindungen zu zwei mqtt-Brokern her.
# In Broker 1 (BrokerSub) wird ein Thema abonniert
# In Broker 2 (BrokerPub) wird ein Thema mit den selben Informationen veröffentlicht

import paho.mqtt.client as mqtt
import configparser
from pathlib import Path

# Definition der Configdatei
ConfigFile = "config.ini"

message = ""

# Prüfen, ob config.ini existiert
# Wenn nein, Default erzeugen

config = configparser.ConfigParser()

if not Path(ConfigFile).is_file():
    print("Konfigurationsdatei nicht vorhanden - Erzeugen einer leeren Datei")
    config['brokersub'] = {'host': '', 'port': '1883','user': '','password': '', 'topic': ''}
    config['brokerpub'] = {'host': '', 'port': '1883','user': '','password': '', 'topic': ''}
    with open(ConfigFile, 'w') as configfile:
        config.write(configfile)
    quit()
else:
    config.read(ConfigFile)

# Definition der Variablen
BrokerSub = config['brokersub']['host']
BrokerSubPort = int(config['brokersub']['port'])
BrokerSubTopic = config['brokersub']['topic']
BrokerSubUser = config['brokersub']['user']
BrokerSubPass = config['brokersub']['password']

BrokerPub = config['brokerpub']['host']
BrokerPubPort = int(config['brokerpub']['port'])
BrokerPubTopic = config['brokerpub']['topic']
BrokerPubUser = config['brokerpub']['user']
BrokerPubPass = config['brokerpub']['password']

def on_connect_sub(client, userdata, flags, rc, properties):
    # Callback-Funktion für die Verbindung zum Broker.
    if rc == 0:
        print(f"Erfolgreich mit dem MQTT-Broker_sub verbunden.")
        client.subscribe(BrokerSubTopic)
        print(f"Abonniert Thema: {BrokerSubTopic}")
    else:
        print(f"Verbindungsfehler. Code: {rc}")

def on_connect_pub(client, userdata, flags, rc, properties):
    global message
    """Callback-Funktion für die Verbindung zum Broker."""
    if rc == 0:
        print("Erfolgreich mit dem MQTT-Broker_pub verbunden.")
        # Nachricht nach erfolgreicher Verbindung veröffentlichen
        #client.disconnect()
    else:
        print(f"Fehler beim Verbinden. Code: {rc}")

def on_message(client, userdata, msg):
    global message
    # Callback-Funktion für eingehende Nachrichten.
    message = msg.payload.decode()
    print(f"Nachricht empfangen: Thema: {msg.topic} | Nachricht: {message}.")
    result = client.publish(BrokerPubTopic, message)
    status = result[0]
    if status == 0:
        print(f"Nachricht '{message}' erfolgreich an Thema '{BrokerPubTopic}' gesendet.")
    else:
        print(f"Fehler beim Senden der Nachricht an Thema '{BrokerPubTopic}'")

def on_publish(client, userdata, mid, rc, properties):
    if rc == 0:
        print(f"Nachricht zum MQTT-Broker {type(client).__name__} erfolgreich gesendet")
    else:
        print(f"Verbindungsfehler. Code: {rc}")


# MQTT-Client einrichten und konfigurieren
client_sub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_sub.username_pw_set(username=BrokerSubUser,password=BrokerSubPass)
client_sub.on_connect = on_connect_sub
client_sub.on_message = on_message

client_pub = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client_pub.username_pw_set(username=BrokerPubUser,password=BrokerPubPass)
client_pub.on_connect = on_connect_pub
#client_pub.on_message = on_message
client_pub.on_publish = on_publish

try:
    print("Verbindungsaufbau zum MQTT-Broker...")
    client_sub.connect(BrokerSub, BrokerSubPort, 60)
    client_pub.connect(BrokerPub, BrokerPubPort, 60)
    
    # Netzwerk-Schleife starten, um Nachrichten zu empfangen
    client_sub.loop_forever()
except KeyboardInterrupt:
    print("\nAbmeldung vom MQTT-Broker und Beenden des Programms...")
    client_sub.disconnect()
    client_pub.disconnect()
except Exception as e:
    print(f"Fehler: {e}")