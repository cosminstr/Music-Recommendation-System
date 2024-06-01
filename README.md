# Image Denoising Machine Learning Model

## Description

Music Recommendation System implemented using K-means Clustering Algorithm with a minimalistic and clean interface. The user can choose to be recommended 10 songs either based on a playlist or on 3 other songs. After submiting the form the user will be redirected to the a spotify playlist with the recommendations.

![alt text](https://github.com/cosminstr/Music-Recommendation-System/blob/main/resources/webapp.png)

## Technologies Used

- Pandas and NumPy for data manipulation
- Sci-Kit Learn for the ML model
- Flask for the Web Application

## Mentions

I plan on modifying the model until i find the best configuration. For finding the right amount of clusters i used the Elbow Method and in order to generate randomness for recommendations i added a little noise to the euclidian distance and selected 10 random songs from the 'closest' 30. I plan on using different datasets to see on which one the model performs best.


