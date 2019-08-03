from Volumio import Volumio

mpd = Volumio('batvolumio')

#mpd.set_volume(17)

mpd.set_playlist('test_python')
mpd.create_playlist()
mpd.record_playlist()

