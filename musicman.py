from sys import argv
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


def download_txt_songs(filename):
    # this will eventually be passing in a *.txt file and searching for
    # each line-item song
    pass
    run(["youtube-dlc", song_title, "--restrict-filenames",
         "--default-search", "gsearch", "-x", "--audio-format",
         "mp3", "--min-views", "1500", "--geo-bypass", "-i",
                "--embed-thumbnail"])
    move_mp3_to_output()