from sys import argv, platform
from pathlib import Path
from tinytag import TinyTag, TinyTagException
from subprocess import run
import os
import shutil
import json
from yt_dlp import YoutubeDL


music_dict = {}

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
            print(
                f"Warning! Found path \n{path} \nhas the same size ({song_size} bytes) as previously found path \n{music_dict[song_size]}")
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


def download_playlist_songs(json_name):
    # if they chose not to put the file extension on, we fix it
    if json_name[-5:] != '.json':
        json_name = json_name + '.json'
    with open(json_name, 'r') as json_file:
        playlists = json.load(json_file)['playlists']
        for playlist in playlists:
            print(f"Downloading songs from {playlist}")
            YDL_OPTIONS = {
                'format': 'bestaudio',
                'geo_bypass': True,
                'restrictfilenames': True,
                'ignoreerrors': True,
                'min_views': 1500,
                'default_search': 'ytsearch',
                'ffmpeg_location': 'C:\\ffmpeg\\bin',
                'playlist_random': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                    {
                    'key': 'FFmpegMetadata'
                }],
                'outtmpl': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'
            }
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download(playlist)


def download_playlist_links(path, link_array):
    """Downloads music from an array into a given path

    Args:
        path (path): The place to 'dump' the files when downloaded
        link_array (string[]): The playlist links to download from
    """
    for playlist in link_array:
        print(f"Downloading songs from {playlist}")
        YDL_OPTIONS = {
            'format': 'bestaudio',
            'geo_bypass': True,
            'restrictfilenames': True,
            'ignoreerrors': True,
            'min_views': 1500,
            'default_search': 'ytsearch',
            'ffmpeg_location': 'C:\\ffmpeg\\bin',
            'playlist_random': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
                {
                'key': 'FFmpegMetadata'
            }],
            'outtmpl': f'{path}\\'+'%(title)s.%(ext)s'
        }
        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download(playlist)


def download_txt_songs(filename):
    # this will eventually be passing in a *.txt file and searching for
    # each line-item song
    # YDL_OPTIONS = {'format': 'bestaudio', 'default_search':'ytsearch'}
    # with YoutubeDL(YDL_OPTIONS) as ydl:
    #     ydl.download(["free bird skynard"])
    # return
    with open(filename, 'r') as songlist:
        all_lines = songlist.readlines()
        YDL_OPTIONS = {
            'format': 'bestaudio',
            'geo_bypass': True,
            'restrictfilenames': True,
            'ignoreerrors': True,
            'min_views': 1500,
            'default_search': 'ytsearch',
            'ffmpeg_location': 'C:\\ffmpeg\\bin',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
                {
                'key': 'FFmpegMetadata'
            }],
            'outtmpl': 'txt_songs/%(title)s.%(ext)s'
        }
        # YDL_OPTIONS = {'format': 'bestaudio'}
        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download(all_lines)


def oscmd():
    if platform.startswith('linux'):
        return "youtube-dlc"
    elif platform == "win32":
        return "youtube-dl.exe"
    else:
        raise Exception("Current OS is neither Windows nor Linux")
