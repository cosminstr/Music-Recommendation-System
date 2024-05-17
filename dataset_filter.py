# Original Dataset had > 1_000_000 entries and my machine couldnt handle it
from app import *

music_data.drop(music_data[music_data['year'].isin([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009])].index, inplace=True)
music_data.drop(music_data[music_data['popularity'] <= 70].index, inplace=True)
# drop() expects indexes as args

music_data.reset_index()
music_data.to_csv('FILTERED_spotify_dataset.csv', index=False)