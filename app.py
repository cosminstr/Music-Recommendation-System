import spotipy
import pandas as pd
import json
from credentials import *
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=MY_SCOPES))

# DATA PREPROCESSING
music_data = pd.read_csv('D:\Projects\Music Recommendation System\dataset.csv')
music_data["explicit"] = music_data["explicit"].astype(int)
music_data = music_data.drop_duplicates()
music_data = music_data.dropna(axis=0)

print(music_data)