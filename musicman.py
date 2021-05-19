from sys import argv, platform
from pathlib import Path
from tinytag import TinyTag, TinyTagException
from subprocess import run
import os
import shutil

music_dict = {}

# Populate this 'youtube playlist links' list to whatever
# playlists you want to download all songs from.
youtube_playlist_links = [
    "https://www.youtube.com/playlist?list=PLRfY4Rc-GWzhdCvSPR7aTV0PJjjiSAGMs"]

# This is the location of which to move files downloaded into the current
# directory
final_destination = "songs_out"
if __name__ == "__main__":
    print("ERROR: Cannot run musicman alone!")


def _populate_music_dict(search_path):
    print("Print dictionary:")
    print(music_dict)
    for path in Path("./").rglob('*.mp3'):
        song_size = os.path.getsize(path)
        if music_dict[song_size] is not None:
            music_dict[song_size] = path
        else:
            print(f"Warning! Found path \n{path} \nhas the same size ({song_size} bytes) as previously found path \n{music_dict[song_size]}")
            print("Thus, skipping newly found song!")
        


def ensure_no_same_songs():
    _populate_music_dict()
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
        run([oscmd(), playlist_link, "--restrict-filenames",
            "--default-search", "gsearch", "-x", "--audio-format",
             "mp3", "--geo-bypass", "-i", "--embed-thumbnail"])


def download_txt_songs(filename):
    # this will eventually be passing in a *.txt file and searching for
    # each line-item song
    with open(filename,'r') as songlist:
        run([oscmd(), songlist.readline(), "--restrict-filenames",
         "--default-search", "gsearch", "-x", "--audio-format",
         "mp3", "--min-views", "1500", "--geo-bypass", "-i",
                "--embed-thumbnail"])


def oscmd():
    currentos = platform.system();
    if currentos == "Linux":
        return "youtube-dlc"
    elif currentos == "Windows":
        return "youtube-dl.exe"
    else:
        raise Exception("Current OS is neither Windows nor Linux")