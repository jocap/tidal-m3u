#!/usr/local/bin/python3

import sys
import tidalapi
import xml.etree.cElementTree as et

config = tidalapi.Config() # quality=tidalapi.Quality.lossless
session = tidalapi.Session(config=config)

try:
    username = sys.stdin.readline().rstrip()
    password = sys.stdin.readline().rstrip()
except KeyboardInterrupt:
    print()
    sys.exit(1)

session.login(username, password)

if not session.check_login():
    sys.stderr.write('login failed\n')
    sys.exit(1)

playlists = session.user.playlists()
selected = False
for playlist in playlists:
    tracks = session.get_playlist_tracks(playlist.id)
    sys.stdout.write('* {}\n'.format(playlist.name))
    with open('{}.m3u'.format(playlist.name), 'w') as f:
        f.write('#EXTM3U\n\n')
        for track in tracks:
            sys.stdout.write('.')
            sys.stdout.flush()
            f.write('#EXTINF:{}, {} - {}\n'.format(track.duration, track.artist.name, track.name))
            f.write('rtmp://{}\n\n'.format(session.get_media_url(track.id)))
    sys.stdout.write('\n')
    sys.stdout.flush()
