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

import musicman
import argparse


__author__ = "Matthew DeTrana"
__license__ = "MIT"
__version__ = "1.0.1"
__status__ = "Development"

# python -m pip install git+https://github.com/blackjack4494/yt-dlc


parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--move", help="Whether or not to move any downloaded songs to a 'songs_out' folder")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-t", "--text", help="Whether or not to download from a provided text file line-by-line", type=str)
group.add_argument(
    "-j", "--json", help="The JSON file containing playlist link(s) to download from", type=str)
args = parser.parse_args()


if args.text:
    musicman.download_txt_songs(args.text.strip())
elif args.json:
    musicman.download_playlist_songs(args.json)
