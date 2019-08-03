from Volumio import Volumio

mpd = Volumio('batvolumio')

#mpd.set_volume(17)

mpd.search('beatles')
mpd.play_song()
#mpd.pause_song()