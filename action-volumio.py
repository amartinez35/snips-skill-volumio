#!/usr/bin/env python3
# coding: utf-8

from hermes_python.hermes import Hermes
from Volumio import Volumio
import requests
import time

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

SLOTS_LIST = [
  'Artist',
  'Song',
  'Piece',
  'VolumioAction'
]

INTENTS_LIST = ['amartinez35:music_action', 'amartinez35:not_music_action']


def intent_received(hermes, intent_message):

  if intent_message.intent.intent_name in INTENTS_LIST:
    available_slots = intent_message.slots
    slots_values = {}
    message = ''

    for slot in SLOTS_LIST:
      if len(available_slots[slot]) > 0:
        slots_values[slot] = available_slots[slot].first().value
      else:
        slots_values[slot] = ''
    
    if len(slots_values['Piece']) == 0:
      slots_values['Piece'] = '192.168.0.25'

    if len(slots_values['VolumioAction']) == 0:
      message = 'Je n\'ai pas compris la demande'
    else:
      mpd = Volumio(slots_values['Piece'])
      action = slots_values['VolumioAction']
      print(action)
      if action == 'demarre':

        song_def = ''
        
        for song_search in ['Song', 'Artist']:

          if len(slots_values[song_search]) > 0:
            print(slots_values[song_search])
            mpd.search(slots_values[song_search])
            song_def = slots_values[song_search]
            break

        time.sleep(1)
        mpd.play_song()
        state = mpd.getState()
        print(state)
        message = 'Je lance la lecture {}'.format(song_def)
      
      if action == 'arrete':
        mpd.pause_song()
        message = 'J\'ai mis la musique en pause'


    hermes.publish_end_session(intent_message.session_id, message)


with Hermes(MQTT_ADDR) as h:
  h.subscribe_intents(intent_received).start()
