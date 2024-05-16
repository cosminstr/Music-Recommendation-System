import spotipy
import pandas as pd
import json
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='5b842c9738454b9a8ed6da1b3daffa31',
                                               client_secret='64222ed18a944e0daeca1e6124819e7a',
                                               redirect_uri='http://localhost:8889/callback',
                                               scope='playlist-read-private'))

# DATA PREPROCESSING
music_data = pd.read_csv('D:\Projects\Music Recommendation System\dataset.csv')
music_data["explicit"] = music_data["explicit"].astype(int)
music_data = music_data.drop_duplicates()
music_data = music_data.dropna(axis=0)

print(music_data)