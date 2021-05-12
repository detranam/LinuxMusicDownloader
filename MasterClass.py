#!/usr/bin/env python

"""Multithreads a music downloader

This allows for multithreading the music downloading script 'b1.sh'.
b1.sh takes in a music list and uses youtube-dl to download the music
(in mp3 file format) to the current directory


LinuxMusicDownloader
Copyright © 2021 Matthew DeTrana

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from sys import argv
from pathlib import Path
from tinytag import TinyTag, TinyTagException
from subprocess import run
import os
import shutil

__author__ = "Matthew DeTrana"
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "detranam.code@gmail.com"
__status__ = "Development"

# python -m pip install git+https://github.com/blackjack4494/yt-dlc

music_dict = {}
# Populate this 'youtube playlist links' list to whatever
# playlists you want to download all songs from.
youtube_playlist_links = [
    "https://www.youtube.com/playlist?list=PLRfY4Rc-GWzhdCvSPR7aTV0PJjjiSAGMs"]

# This is the location of which to move files downloaded into the current
# directory
final_destination = "songs_out"


def populate_music_dict(search_path):
    print("Print dictionary:")
    print(music_dict)


def ensure_no_same_songs():
    if len(music_dict) == 0:
        print("ERROR: No values in the song dictionary.")
        return

    # TODO: find an efficient algorithm to go through and check
    # to see if a song is unique via tag.size (in bytes).

    # I'm thinking start at the beginning then compare each item
    # to all following values, then creating a list of 'conflicts',
    # which are just the same size song.

    # I'd also like to ensure no same-name songs, that's a problem
    # for future me, though.


def move_mp3_to_output():
    create_dir(final_destination)
    for path in Path("./").rglob('*.mp3'):
        shutil.move(path, final_destination)


def create_dir(newdir):
    try:
        os.mkdir(newdir)
        print(f"Creating directory '{newdir}'!")
    except FileExistsError:
        print(f"Directory '{newdir}' already exists!")


def download_playlist_songs():
    print("Downloading playlist songs")
    for playlist_link in youtube_playlist_links:
        run(["youtube-dlc", playlist_link, "--restrict-filenames",
            "--default-search", "gsearch", "-x", "--audio-format",
             "mp3", "--geo-bypass", "-i", "--embed-thumbnail"])
    move_mp3_to_output()


def download_txt_songs():
    # this will eventually be passing in a *.txt file and searching for
    # each line-item song
    pass
    run(["youtube-dlc", song_title, "--restrict-filenames",
         "--default-search", "gsearch", "-x", "--audio-format",
         "mp3", "--min-views", "1500", "--geo-bypass", "-i",
                "--embed-thumbnail"])
    move_mp3_to_output()


if __name__ == "__main__":
    try:
        download_playlist_songs()
        # move_mp3_to_output()
        # download_new_songs()
        # populate_music_dict(argv[1])
    except TinyTagException as err:
        print("ERROR: TinyTag threw an error: " + err)