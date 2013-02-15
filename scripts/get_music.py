#!/usr/bin/python
# Copies an album from an ipod into the appropriate spot on my external.

import os
import subprocess
import sys

IPOD = '/mnt/tmp'
DEST = '/mnt/hd/files/music'

if len(sys.argv) != 3:
  print('Usage: ./get_music.py <artist> <album>')
  sys.exit(1)

artist = sys.argv[1]
album = sys.argv[2]

search_proc = subprocess.Popen(['gnupod_search.pl', 
                                '--mount={0}'.format(IPOD),
                                '--artist={0}'.format(artist),
                                '--album={0}'.format(album), 
                                '--view=ntu'
                               ],
                               stdout=subprocess.PIPE)

stdoutdata,stderrdata = search_proc.communicate()

music = stdoutdata.split('\n')
dest_dir = '{0}/{1}/{2}/'.format(DEST, artist, album)
try:
  os.makedirs(dest_dir)
except:
  pass

for line in music[3:]:
  if line:
    values = [x.rstrip() for x in line.split('|')]
    track_num = values[0].zfill(2)
    title = values[1].replace('/', '_')
    path = values[2]
    dest = dest_dir + '{0}-{1}.mp3'.format(track_num, title)
    print('cp "{0}" "{1}"'.format(path, dest))
    subprocess.check_call(['cp', path, dest]) 
