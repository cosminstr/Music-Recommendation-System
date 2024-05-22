import spotipy
import pandas as pd
import numpy as np
import json
from credentials import *
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=MY_SCOPES))

music_data: pd.DataFrame = pd.read_csv('D:\Projects\Music Recommendation System\FILTERED_spotify_dataset3.csv')
# Drop unwanted features
music_data.drop(columns=['Unnamed: 0'], inplace=True)
music_data.drop(columns=['time_signature'], inplace=True)
music_data = music_data.drop_duplicates()
music_data = music_data.dropna(axis=0)

# User's songs
songs_data_list: list = []

if __name__ == "__main__":

    i: int = 3
    no: int = 0

    print(f'Hi! I am a Music Recommendation System!\nI will suggest 10 songs based on 3 others you like!\n')
    
    # looping until it finds 3 valid songs
    while no != i:

        print(f"{no + 1}) Pick a Track:")
        user_song = input().strip()
        print('Choose the Artist:')
        user_artist = input().strip()

        results = sp.search(q=f"track:{user_song} artist:{user_artist}", limit=1, type='track')

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
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
            no = no + 1
        else:
            print('This track doesnt exit')

    # created the dataframe with a list of dictionaries instead of adding another entry in a df every time
    user_songs_features = pd.DataFrame(songs_data_list)

    scaler = StandardScaler()

    music_data_aux = music_data.select_dtypes(np.number)
    user_songs_aux = user_songs_features.select_dtypes(np.number)    


    scaled_data = scaler.fit_transform(music_data_aux.values)
    scaled_user_data = scaler.transform(user_songs_aux.values)

    scaled_music_data = pd.DataFrame(scaled_data, columns=music_data_aux.columns)
    scaled_user_songs = pd.DataFrame(scaled_user_data, columns= user_songs_aux.columns)

    spotify_music_data = pd.concat([music_data[['artist_name', 'track_name', 'track_id']], scaled_music_data], axis=1)
    user_songs_data = pd.concat([user_songs_features[['artist_name', 'track_name', 'track_id']], scaled_user_songs], axis = 1)
    
    # print(spotify_music_data)
    # print(user_songs_data)

    # K-means clustering
    seed = np.random.randint(35, 40)

    kmeans = KMeans(n_clusters=10, random_state=seed).fit(scaled_music_data)
    spotify_music_data['cluster'] = kmeans.labels_

    user_clusters = kmeans.predict(scaled_user_songs)
    common_cluster = np.bincount(user_clusters).argmax()
    cluster_songs = spotify_music_data[spotify_music_data['cluster'] == common_cluster]
    cluster_song_features = cluster_songs.drop(columns=['artist_name', 'track_name', 'track_id', 'cluster'])
    distances = euclidean_distances(scaled_user_songs, cluster_song_features)
    mean_distances = distances.mean(axis=0)
    cluster_songs['distance'] = mean_distances

    recommended_songs = cluster_songs.nsmallest(10, 'distance')

    print("Recommended Songs:")
    # print(recommended_songs[['artist_name', 'track_name', 'track_id']])

    playlist = sp.user_playlist_create('21zrpk5i6zoo65pixpej6emci', 'Recomandari', public=True)
    sp.user_playlist_add_tracks('21zrpk5i6zoo65pixpej6emci', playlist['id'], recommended_songs['track_id'])
    print(playlist['external_urls']['spotify'])