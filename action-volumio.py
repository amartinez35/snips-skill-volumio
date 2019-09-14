#!/usr/bin/env python3
# coding: utf-8

from hermes_python.hermes import Hermes
import requests


MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def intent_received(hermes, intent_message):

  if intent_message.intent.intent_name == 'amartinez35:music_action' or intent_message.intent.intent_name == 'amartinez35:not_music_action' :
    print(intent_message.slots.Artist.first().value)



with Hermes(MQTT_ADDR) as h:
  h.subscribe_intents(intent_received).start()
