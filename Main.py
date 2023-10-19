import Spotify_API
import Email_Sending
import schedule
import time
import datetime

playlist_id = "3U9lafWEnb3uP6JFbI65uq"
subject = "New Playlist Update on Spotify"
email_sender = "jd.doellinger@gmail.com"
email_receiver = "julius.doellinger@gmx.de"

playlist_songs = Spotify_API.get_playlist_items(playlist_id)
updated_songs = Spotify_API.filter_for_update(playlist_songs)

if not updated_songs:
    print("no updates")
else:
    formatted_list = [f"Track Name: {item['Track Name']}, Artist(s): {', '.join(item['Artist(s)'])}" for item in updated_songs]
    body = '\n'.join(formatted_list)
    Email_Sending.sendEmail(subject, body, email_sender, email_receiver)