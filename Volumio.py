import subprocess
import time
# pour la communication avec volumio
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace

class Volumio:

    def __init__(self, server='localhost', port=3000):
        # connection vers volumio
        self.socketIO = SocketIO(server, port)
   
    def __on_getQueue_response(self, *args):
        self.playlist = args[0]

    def __on_search_response(self, *args):
        search_result = args[0].get('navigation').get('lists')[0].get('items')[0].get('uri')
        print(search_result)
        self.clear_queue()
        self.add_to_queue(search_result)

    def __on_getState_response(self, *args):
        print(args[0])

    def set_playlist(self, playlist):
        self.playlist_name = playlist
        self.socketIO.on('pushQueue', self.__on_getQueue_response)
        self.socketIO.emit('getQueue', '', self.__on_getQueue_response)
        self.socketIO.wait_for_callbacks(seconds=1)
    
    def play_playlist(self):
        self.socketIO.emit('playPlaylist', {'name': self.playlist_name})
    
    def create_playlist(self):
        self.socketIO.emit('createPlaylist', {'name': self.playlist_name})
    
    def remove_playlist(self):
        self.socketIO.emit('deletePlaylist', {'name': self.playlist_name})
    
    def set_volume(self, volume):
        if volume > 0 or volume <100:
          self.socketIO.emit('volume', volume)
    
    def add_to_playlist(self, song):
        uri = song['uri']
        self.socketIO.emit('addToPlaylist', {'name': self.playlist_name, 'service': song['service'], 'uri': uri})
    
    def record_playlist(self):
        for song in self.playlist:
            self.add_to_playlist(song)
            time.sleep(0.7)

    def search(self, query):
        self.socketIO.on('pushBrowseLibrary', self.__on_search_response)
        self.socketIO.emit('search', {'value': query}, self.__on_search_response)
        self.socketIO.wait_for_callbacks(seconds=1)

    def getState(self):
        self.socketIO.on('pushState', self.__on_getState_response)
        self.socketIO.emit('getState', '', self.__on_getState_response)
        self.socketIO.wait_for_callbacks(seconds=1)

    
    def next_song(self):
        self.socketIO.emit('next')
    
    def previous_song(self):
        self.socketIO.emit('prev')
    
    def stop_song(self):
        self.socketIO.emit('stop')
    
    def pause_song(self):
        self.socketIO.emit('pause')
    
    def play_song(self):
        self.socketIO.emit('play')
    
    def clear_queue(self):
        self.socketIO.emit('clearQueue')
    
    def add_to_queue(self, uri):
        self.socketIO.emit('addToQueue', {'uri': uri})
    

    @staticmethod
    def shutdown():
        subprocess.call(['shutdown', '-h', 'now'], shell=False)