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

INTENT_PLAY = 'amartinez35:play_music'
INTENT_STOP = 'amartinez35:stop_music'

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
            'config.ini',
            encoding = 'utf-8'
        ) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error):
        return dict()

def get_room(intent_message):
  print(intent_message.slots.Piece)
  

def intent_paly_music(hermes, intent_message):
  message = ''
  hermes.publish_end_session(intent_message.session_id, message)
  return True

def intent_stop_music(hermes, intent_message):
  message = 'J\'ai mis la musique en pause'
  get_room(intent_message)
  hermes.publish_end_session(intent_message.session_id, message)
  return True

if __name__ == '__main__':
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent(INTENT_PLAY, intent_paly_music) \
         .subscribe_intent(INTENT_STOP, intent_stop_music) \
         .loop_forever()

