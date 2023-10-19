import json
import requests
from requests import post, get
import os
import base64
import datetime

client_id = "a6fe8954c7524fedb4596fb3a23739a7"
client_secret = "6faf6f4260e34f678940b31c6a1791ff"
redirect_uri = "http://localhost:your_port/callback"
playlist_id = "3U9lafWEnb3uP6JFbI65uq"

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data =  {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_playlist_items(playlist_id):
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the response to get information about the tracks in the playlist.
        playlist_data = response.json()

        track_list = []

        for item in playlist_data['items']:
            track = item['track']
            added_at = item['added_at']
            track_info = {
                "Track Name": track['name'],
                "Artist(s)": [artist['name'] for artist in track['artists']],
                "Added At": added_at
            }
            track_list.append(track_info)
        return track_list
    else:
        print(f"Failed to retrieve playlist items. Status code: {response.status_code}")

def filter_for_update(track_list):
    end_date = datetime.datetime.now()
    due_date = end_date - datetime.timedelta(days=4)
    filtered_tracks = []
    for track in track_list:
        # Convert the "Added At" string to a datetime object
        added_at_date = datetime.datetime.fromisoformat(track["Added At"][:-1])

        if added_at_date >= due_date:
            filtered_tracks.append(track)
    return filtered_tracks


