import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt

# the code commented below was only used once to measure the right value for the number of clusters

# sum_of_squared_distances = []

# for k in range(1, 20):
#     kmeans = KMeans(n_clusters=k, random_state=40).fit(scaled_music_data)
#     sum_of_squared_distances.append(kmeans.inertia_)

# plt.plot(range(1, 20), sum_of_squared_distances, 'bx-')
# plt.show()

# kmeans clustering

def recommend_alg(dataset_songs_scaled, user_songs_scaled, dataset_songs) -> pd.DataFrame:

    kmeans = KMeans(n_clusters=8).fit(dataset_songs_scaled)
    dataset_songs['cluster'] = kmeans.labels_

    user_songs_clusters = kmeans.predict(user_songs_scaled)
    common_cluster = np.bincount(user_songs_clusters).argmax()
    dataset_cluster_songs = dataset_songs[dataset_songs['cluster'] == common_cluster]
    dataset_cluster_song_features = dataset_cluster_songs.drop(columns=['artist_name', 'track_name', 'track_id', 'cluster'])

    # adding small noise to the distances for randomness
    distances = euclidean_distances(user_songs_scaled, dataset_cluster_song_features)
    mean_distances = distances.mean(axis=0)
    noise = np.random.normal(0, 0.01, mean_distances.shape)
    dataset_cluster_songs['distance'] = mean_distances + noise

    # picking 10 random songs from the closest 30 for increased randomness
    top_30_songs = dataset_cluster_songs.nsmallest(30, 'distance')
    recommended_songs = top_30_songs.sample(10)

    return recommended_songs