from sys import argv, platform
from pathlib import Path
import subprocess
import os
import shutil
import json
from yt_dlp import YoutubeDL
import logging

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
            #paste this back in if failures
            #                'ffmpeg_location': 'C:\\ffmpeg\\bin',

            print(f"Downloading songs from {playlist}")
            YDL_OPTIONS = {
                'format': 'bestaudio',
                'geo_bypass': True,
                'restrictfilenames': True,
                'ignoreerrors': True,
                'min_views': 1500,
                'ffmpeg_location': 'bin',
                'default_search': 'ytsearch',
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


def get_new_songs_to_dl(playlist_link, already_downloaded_list):
    try:
        output = subprocess.check_output(["yt-dlp","-s", f"{playlist_link}"], stderr=subprocess.STDOUT).decode('utf-8') #.exe
    except subprocess.CalledProcessError as er:
        logging.error(f"Download from playlist failed, likely an incorrect song. RETURN CODE:{er.returncode}")
        output = er.output.decode('utf-8')
    splitlines = output.split("\n")
    useful_lines = []
    playlist_id = ""
    for line in splitlines:
        if line.find('[youtube:tab]') != -1:
            if line.find('Downloading webpage') != -1:
                #'[youtube:tab] PLmi9g6uwZPL-kvPX9aJhMEpGM_KHcgjSX: Downloading webpage'
                playlist_id = (line.replace("[youtube:tab] ", "")).replace(": Downloading webpage","")
                continue
            continue
        if line.find('Downloading video') != -1:
            continue
        if line.find('youtube:tab') != -1:
            continue
        if line.find('Downloading webpage') != -1:
            useful_lines.append(line)

    # at this point, useful_lines should only have what we want in it
    cleaned_useful_lines = []
    for line in useful_lines:
        cleaned_useful_lines.append((line.replace("[youtube] ", "")).replace(": Downloading webpage",""))
    #now we find all the unique codes in cleaned_useful_lines that are not in already_downloaded_list, and return it with the playlist ID

    new_song_ids = []
    for code in cleaned_useful_lines:
        if code in already_downloaded_list:
            continue
        new_song_ids.append(code)


    return new_song_ids,playlist_id


def download_playlist_atomic(path, starting_playlist_str):
    """Downloads music from an array into a given path

    Args:
        path (path): The place to 'dump' the files when downloaded
        playlist_likm (string): The playlist link to download
    """

    already_dld_songs = starting_playlist_str.split(',')
    playlist_link = already_dld_songs[0]
    individual_new_songs_to_dl, playlist_id = get_new_songs_to_dl(playlist_link, already_dld_songs)
    if len(individual_new_songs_to_dl) == 0:
        print(f"No new songs to download for playlist link {playlist_link}")
        return ""
    print(f"Downloading {len(individual_new_songs_to_dl)} new songs from {playlist_link}")
    for code in individual_new_songs_to_dl:
        YDL_OPTIONS = {
            'format': 'bestaudio',
            'geo_bypass': True,
            'restrictfilenames': True,
            'ignoreerrors': True,
            'min_views': 1500,
            'default_search': 'ytsearch',
            'ffmpeg_location': 'bin',
            'playlist_random': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
                {
                'key': 'FFmpegMetadata'
            }],
            'outtmpl': f'{path}/'+ f"{playlist_id}/"  +'%(title)s.%(ext)s'
        }
        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download("https://www.youtube.com/watch?v=" + code)#playlist_link)
    #now that we've downloaded all the codes, we should update the playlist link by appending all the new song codes we just downloaded
    updated_codes = ','.join(already_dld_songs + individual_new_songs_to_dl)
    return updated_codes
    #now that we finished downloading all our songs, return the new and edited link_array in order for state to be saved.
    return ret_dict

def download_playlist_links(path, link_array):
    """Downloads music from an array into a given path

    Args:
        path (path): The place to 'dump' the files when downloaded
        link_array (string[]): The playlist links to download from
    """

    ret_dict = {}
    for playlist in link_array:
        already_dld_songs = playlist.split(',')
        playlist_link = already_dld_songs[0]
        individual_new_songs_to_dl, playlist_id = get_new_songs_to_dl(playlist_link, already_dld_songs)
        if len(individual_new_songs_to_dl) == 0:
            print(f"No new songs to download for playlist link {playlist_link}")
            continue
        print(f"Downloading {len(individual_new_songs_to_dl)} new songs from {playlist_link}")
        for code in individual_new_songs_to_dl:
            YDL_OPTIONS = {
                'format': 'bestaudio',
                'geo_bypass': True,
                'restrictfilenames': True,
                'ignoreerrors': True,
                'min_views': 1500,
                'default_search': 'ytsearch',
                'ffmpeg_location': 'bin',
                'playlist_random': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                    {
                    'key': 'FFmpegMetadata'
                }],
                'outtmpl': f'{path}\\'+ f"{playlist_id}\\"  +'%(title)s.%(ext)s'
            }
            with YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download("https://www.youtube.com/watch?v=" + code)#playlist_link)
        #now that we've downloaded all the codes, we should update the playlist link by appending all the new song codes we just downloaded
        updated_codes = ','.join(already_dld_songs + individual_new_songs_to_dl)
        ret_dict[playlist_link] = updated_codes
    #now that we finished downloading all our songs, return the new and edited link_array in order for state to be saved.
    return ret_dict

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
            'ffmpeg_location': 'bin',
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
