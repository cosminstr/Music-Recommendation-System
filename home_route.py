from flask import render_template, request, redirect
from app import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from model import recommend_alg

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=MY_SCOPES))

music_data: pd.DataFrame = pd.read_csv('D:\Projects\Music Recommendation System\spotify_dataset3.csv')

# drop unwanted features
music_data.drop(columns=['Unnamed: 0'], inplace=True)
music_data.drop(columns=['time_signature'], inplace=True)
music_data = music_data.drop_duplicates()
music_data = music_data.dropna(axis=0)

# user's songs
songs_data_list: list = []
results = []

@app.route('/', methods=['GET', 'POST'])

def home():

    if request.method == 'POST':
        
        # extract the data if the user did not submbit a playlist
        if not request.form.get('playlist'):
            results1 = sp.search(q=f"track:{request.form['song1']} artist:{request.form['artist1']}", limit=1, type='track')
            results.append(results1)
            results2 = sp.search(q=f"track:{request.form['song2']} artist:{request.form['artist2']}", limit=1, type='track')
            results.append(results2)
            results3 = sp.search(q=f"track:{request.form['song3']} artist:{request.form['artist3']}", limit=1, type='track')
            results.append(results3)

            for result in results: 
                if result['tracks']['items']:
                    track = result['tracks']['items'][0]
                    track_id = track['id']
                    audio_features = sp.audio_features(track_id)
                    track_info = sp.track(track_id)

                    song_data = {
                        'artist_name': track_info['album']['artists'][0]['name'],
                        'track_name': track_info['name'],
                        'track_id': track_id,
                        'popularity': track_info['popularity'],
                        'year': int(track_info['album']['release_date'].split('-')[0]),
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
                        'duration_ms': track_info['duration_ms']
                        # 'time_signature': audio_features[0]['time_signature']
                    }

                    songs_data_list.append(song_data)

        # extract the data if the user did submit a playlist
        else:

            def fetch_playlist_tracks(playlist_id):
                offset = 0
                tracks = []
                while True:
                    results = sp.playlist_tracks(playlist_id, offset=offset)
                    tracks += results['items']
                    if len(results['items']) == 0:
                        break
                    offset += len(results['items'])
                return tracks

            playlist_tracks = fetch_playlist_tracks(request.form['playlist'])

            for track in playlist_tracks:
                track = track['track']
                track_id = track['id']
                audio_features = sp.audio_features(track_id)
                track_info = sp.track(track_id)

                song_data = {
                    'artist_name': track_info['album']['artists'][0]['name'],
                    'track_name': track_info['name'],
                    'track_id': track_id,
                    'popularity': track_info['popularity'],
                    'year': int(track_info['album']['release_date'].split('-')[0]),
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
                    'duration_ms': track_info['duration_ms']
                    # 'time_signature': audio_features[0]['time_signature']
                }

                songs_data_list.append(song_data)

        # created the dataframe with a list of dictionaries instead of adding another entry in a df every time
        user_songs_features = pd.DataFrame(songs_data_list)


        # scaling down the numeric values before applying the algorithm
        scaler = StandardScaler()
        music_data_aux = music_data.select_dtypes(np.number)
        user_songs_aux = user_songs_features.select_dtypes(np.number)    

        scaled_data = scaler.fit_transform(music_data_aux.values)
        scaled_user_data = scaler.transform(user_songs_aux.values)

        scaled_music_data_df = pd.DataFrame(scaled_data, columns=music_data_aux.columns)
        scaled_user_songs_df = pd.DataFrame(scaled_user_data, columns= user_songs_aux.columns)

        spotify_music_data = pd.concat([music_data[['artist_name', 'track_name', 'track_id']], scaled_music_data_df], axis=1)
        user_songs_data = pd.concat([user_songs_features[['artist_name', 'track_name', 'track_id']], scaled_user_songs_df], axis = 1)
        
        # print(spotify_music_data)
        # print(user_songs_data)

        recommended_songs = recommend_alg(dataset_songs_scaled=scaled_music_data_df, 
                                    user_songs_scaled=scaled_user_songs_df,
                                    dataset_songs=spotify_music_data)

        # print("Recommended Songs:")
        # print(recommended_songs[['artist_name', 'track_name', 'track_id']])

        # 21zrpk5i6zoo65pixpej6emci is my spotify public id
        playlist = sp.user_playlist_create('21zrpk5i6zoo65pixpej6emci', 'Recomandari', public=True)
        sp.user_playlist_add_tracks('21zrpk5i6zoo65pixpej6emci', playlist['id'], recommended_songs['track_id'])
        # print(playlist['external_urls']['spotify'])
        return redirect(playlist['external_urls']['spotify'])
    else:
        return render_template('index.html')