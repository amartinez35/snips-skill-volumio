#!/usr/bin/env python3
# coding: utf-8

from hermes_python.hermes import Hermes
from Volumio import Volumio
import requests
import json


MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


def intent_received(hermes, intent_message):

  if intent_message.intent.intent_name == 'amartinez35:music_action' or intent_message.intent.intent_name == 'amartinez35:not_music_action':
    available_slots = json.loads(intent_message.custom_data)

    artist = intent_message.slots.Artist.first().value or available_slots['Artist']
    song = intent_message.slots.Song.first().value or available_slots['Song']
    album = intent_message.slots.Album.first().value or available_slots['Album']
    piece = intent_message.slots.Piece.first().value or available_slots['Piece']
    action = intent_message.slots.VolumioAction.first().value or available_slots['VolumioAction']

    message = ''
    if not action:
      message = 'Je n\' pas compris'
    
    if not piece:
      piece = '192.168.0.25'

    
    mpd = Volumio(piece)
    mpd.search(artist)
    mpd.play_song()

    hermes.publish_end_session(intent_message.session_id, 'J\'ai mis {}'.format(artist))


with Hermes(MQTT_ADDR) as h:
  h.subscribe_intents(intent_received).start()
