#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Get the songs list from a spotify public playlist and write it down to a file.
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# You should set environtment variables outside python. To get app client see: https://developer.spotify.com
os.environ["SPOTIPY_CLIENT_ID"] = "your-spotify-client-id"
os.environ["SPOTIPY_CLIENT_SECRET"] = "your-spotify-client-secret"

DATA_FILE = "song_list.txt"  # change this as you need

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def write_file(song_list):
    """Write a file with songs list.

    Parameters
    ----------
    song_list : object
        The song_list to write down.
    """

    with open(DATA_FILE, "a", encoding="utf-8") as temp_file:
        for song in song_list:
            temp_file.write(song[0] + " " + song[1] + "\n")


def get_playlist_tracks(username, playlist_id):
    """Get the tracks items from spotify.

    Parameters
    ----------
    username : string
        owner of the playlist
    playlist_id : string
        playlist id see: https://developer.spotify.com/documentation/web-api/#spotify-uris-and-ids
    """
    results = spotify.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks


def get_tracks(playlist_tracks):
    """Map song name and artist name from a track item.

    Parameters
    ----------
    playlist_tracks : list
        tracks items
    """
    return playlist_tracks['track']['name'], playlist_tracks['track']['artists'][0]['name']


if __name__ == '__main__':

    # Specify the data of the playlist you want to get

    username = "valid-username"  # i.e. spotify
    playlist_id = "valid-playlist-id"  # i.e. 37i9dQZF1DXcBWIGoYBM5M

    playlist_tracks = get_playlist_tracks(username, playlist_id)

    tracks = list(map(get_tracks, playlist_tracks))

    write_file(tracks)
