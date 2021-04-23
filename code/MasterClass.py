#!/usr/bin/env python

"""Multithreads a music downloader

This allows for multithreading the music downloading script 'b1.sh'.
b1.sh takes in a music list and uses youtube-dl to download the music
(in mp3 file format) to the current directory

Copyright 2019 Matthew DeTrana

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
#from multiprocessing.dummy import Pool as ThreadPool

#from os import listdir
#from os.path import isfile, join
from sys import argv
#from glob import glob
from pathlib import Path

__author__ = "Matthew DeTrana"
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__email__ = "detranam.code@gmail.com"
__status__ = "Development"

_path_to_search = "search_me"

def list_files(search_path):
  onlyfiles = []
  for path in Path(search_path).rglob('*.*'):
    onlyfiles.append(path)
  print("printing files")
  print(onlyfiles)

if __name__ == "__main__":
  print("calling main")
  list_files(argv[1])