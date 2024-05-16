import spotipy
import pandas as pd
import numpy as np
import json
from credentials import *
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import StandardScaler

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=MY_SCOPES))

# DATA PREPROCESSING
music_data: pd.DataFrame = pd.read_csv('D:\Projects\Music Recommendation System\spotify_dataset.csv')
music_data = music_data.drop_duplicates()
music_data = music_data.dropna(axis=0)

scaler = StandardScaler()
music_data = music_data.select_dtypes(np.number)


scaled_X = scaler.fit_transform(music_data.values)

scaled_music_data = pd.DataFrame(scaled_X,
                        columns=music_data.columns)


