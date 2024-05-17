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
music_data: pd.DataFrame = pd.read_csv('D:\Projects\Music Recommendation System\FILTERED_spotify_dataset2.csv')
music_data.drop(columns=['Unnamed: 0'], inplace=True)
music_data = music_data.drop_duplicates()
music_data = music_data.dropna(axis=0)

if __name__ == "__main__":
    # while True:
    print("Pick a track:")
    user_song = input().strip()
    print('Choose the Artist')
    user_artist = input().strip()

    results = sp.search(q=f"track:{user_song} artist:{user_artist}", limit=1, type='track')

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_id = track['id']
        audio_features = sp.audio_features(track_id)
        track_info = sp.track(track_id)

    else:
        print('Nu exista acest track')

        # print("Continuam? (Y/N)")
        # r = input().strip()

        # if r == 'N':
        #     break
        # elif r == 'Y': pass
        # else: 'Comanda invalida'

    song_data = {
        'popularity': track_info['popularity'],
        'year': track_info['album']['release_date'].split('-')[0],
        'danceability': audio_features[0]['danceability'],
        'energy': audio_features[0]['energy'],
        'key': audio_features[0]['key'],
        'loudness': audio_features[0]['loudness'],
        'mode': audio_features[0]['mode'],
        'speechiness': audio_features[0]['speechiness'],
        'acousticness': audio_features[0]['acousticness'],
        'instrumentalness': audio_features[0]['instrumentalness'],
        'liveness': audio_features[0]['liveness'],
        'valence': audio_features[0]['valence'],
        'tempo': audio_features[0]['tempo'],
        # 'explicit': track_info['explicit'],
        'duration_ms': track_info['duration_ms'],
        'time_signature': audio_features[0]['time_signature']
    }

    user_song_features = pd.DataFrame(song_data, index=[0])

    print(user_song_features)

    # Scale down the values before applying Kmeans 
    scaler = StandardScaler()
    music_data_aux = music_data.select_dtypes(np.number)

    scaled_data = scaler.fit_transform(music_data_aux.values)

    scaled_music_data = pd.DataFrame(scaled_data,
                            columns=music_data_aux.columns)
    
    # Adding the str columns to the scaled down dataframe
    spotify_music_data = pd.concat([music_data[['artist_name', 'track_name', 'track_id']], scaled_music_data], axis=1)
    
    print(spotify_music_data)

    # user_song_features IS NOT SCALED DOWN
