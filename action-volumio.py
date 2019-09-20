#!/usr/bin/env python3
# coding: utf-8
import json
import configparser
import io
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
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


class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {
            section: {
                option_name: option
                for option_name, option in self.items(section)
            }
            for section in self.sections()
        }


def read_configuration_file():
    try:
        with io.open(
            "config.ini",
            encoding="utf-8"
        ) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error):
        return dict()

def get_room(room):
  config = read_configuration_file()
  if len(room) == 0:
    return config['secret']['salon']
  return room

def read_slots(intent_message):
  available_slots = intent_message.slots
  slots_values = {}

  for slot in SLOTS_LIST:
    if len(available_slots[slot]) > 0:
      slots_values[slot] = available_slots[slot].first().value
    else:
      slots_values[slot] = '' 
  
  return slots_values



def intent_received(hermes, intent_message):

  if intent_message.intent.intent_name in INTENTS_LIST:
    slots_values = read_slots(intent_message)
    message = ''

    room = get_room(slots_values['Piece'])

    if len(slots_values['VolumioAction']) == 0:
      message = 'Je n\'ai pas compris la demande'
    else:
      mpd = Volumio(room)
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
        #state = mpd.getState()
        #print(state)
        #print(song_def)
        message = 'Je lance la lecture {}'.format(song_def)
      
      if action == 'arrete':
        mpd.pause_song()
        message = 'J\'ai mis la musique en pause'


    hermes.publish_end_session(intent_message.session_id, message)

if __name__ == '__main__':
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents(intent_received).start()

