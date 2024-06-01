# the original dataset had > 1_000_000 entries and my machine couldnt handle it
from home_route import music_data

music_data.drop(music_data[music_data['year'].isin([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007])].index, inplace=True)
music_data.drop(music_data[music_data['popularity'] <= 50].index, inplace=True)
# drop() expects indexes as args

music_data.reset_index()
music_data.to_csv('FILTERED_spotify_dataset3.csv', index=False)
# change the path to the file in app.py after exporting to csv as well