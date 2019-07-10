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

    def set_playlist(self, playlist):
        self.playlist_name = playlist
        self.socketIO.on('pushQueue', self.__on_getQueue_response)
        self.socketIO.emit('getQueue', '', self.__on_getQueue_response)
        self.socketIO.wait_for_callbacks(seconds=1)
    
    def play_playlist(self):
        self.socketIO.emit('playPlaylist', {'name': self.playlist_name})
    
    def create_playlist(self):
        self.socketIO.emit('createPlayist', {'name': self.playlist_name})
    
    def remove_playlist(self):
        self.socketIO.emit('deletePlaylist', {'name': self.playlist_name})
    
    def set_volume(self, volume):
        (self.socketIO.emit('mute', ''), self.socketIO.emit('volume', volume))[volume<=100 and volume>=0]
    
    def add_to_playlist(self, song):
        uri = song['uri'].decode().encode('utf-8')
        self.socketIO.emit('addToPlaylist', {'name': self.playlist_name, 'service': song['service'], 'uri': uri})
    
    def record_playlist(self):
        for song in self.playlist:
            self.add_to_playlist(song)
            time.sleep(0.7)
    
    def next_song(self):
        self.socketIO.emit('next', '')
    
    def previous_song(self):
        self.socketIO.emit('prev', '')
    
    def stop(self):
        self.socketIO.emit('stop', '')
    
    def play(self):
        self.socketIO.emit('play', '')
    
    def clear_queue(self):
        self.socketIO.emit('clearQueue', '')
    

    @staticmethod
    def shutdown():
        subprocess.call(['shutdown', '-h', 'now'], shell=False)