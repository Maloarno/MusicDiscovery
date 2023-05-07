import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import pyarrow as pa
import pyarrow.parquet as pq

# Spotify Data

# Spotify API credentials
client_id = '651c908112b04c008f843b0fa3475186'
client_secret = 'd458245047e54d22bbcc7af4ba51031f'

# Spotify artist URI
artist_uri = 'spotify:artist:4tZwfgrHOc3mvqYlEYSvVi'

# Authenticate with Spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

def fetch_top_tracks(year, limit=50):
    data = []
    # Query tracks for given year in batches of 50
    for i in range(0, limit, 50):
        track_results = spotify.search(q=f'year:{year}', type='track', limit=50, offset=i)
        # Extract relevant track information and audio features
        for j, track in enumerate(track_results['tracks']['items']):
            item = {}
            item['rank'] = i+j+1
            item['artist'] = track['artists'][0]['name']
            item['album'] = track['album']['name']
            item['track'] = track['name']
            item['danceability'] = spotify.audio_features(track['id'])[0]['danceability']
            item['loudness'] = spotify.audio_features(track['id'])[0]['loudness']
            item['popularity'] = track['popularity']
            item['available_markets'] = len(track['available_markets'])
            item['duration_ms'] = track['duration_ms']
            item['energy'] = spotify.audio_features(track['id'])[0]['energy']
            item['key'] = spotify.audio_features(track['id'])[0]['key']
            item['mode'] = spotify.audio_features(track['id'])[0]['mode']
            item['speechiness'] = spotify.audio_features(track['id'])[0]['speechiness']
            item['acousticness'] = spotify.audio_features(track['id'])[0]['acousticness']
            item['instrumentalness'] = spotify.audio_features(track['id'])[0]['instrumentalness']
            item['liveness'] = spotify.audio_features(track['id'])[0]['liveness']
            item['valence'] = spotify.audio_features(track['id'])[0]['valence']
            item['platform'] = 'Spotify'
            data.append(item)
    return pd.DataFrame(data)

# Write dataframe to Parquet file
def save_dataframe_to_parquet(dataframe, filename): 
    pq.write_table(pa.Table.from_pandas(dataframe), filename)

# Load dataframe from Parquet file
def load_dataframe_from_parquet(filename):
    return pq.read_table(filename).to_pandas()

# Fetch top 50 tracks from year 2023
spotify_data = fetch_top_tracks(2023, 50)

# Save data to Parquet file
save_dataframe_to_parquet(spotify_data, 'spotify_data.parquet')

#################################################################################################################

# Deezer Data

# Set the Deezer API endpoint URL and parameters
api_url = 'https://api.deezer.com/search'
api_params = {
    'q': 'year:2018',
    'type': 'track',
    'limit': 50,
}

# Set the headers to include the API key
api_headers = {
    'x-rapidapi-host': 'https://developers.deezer.com/myapps/app/601084',
    'x-rapidapi-key': '3e678ee2516677d0c092634065eef4f3',
}

# Make the API requests and collect data in a list of dictionaries
data = []
for i in range(0, 500, 50):
    api_params['index'] = i
    response = requests.get(api_url, headers=api_headers, params=api_params)
    if response.status_code == 200:
        for j, t in enumerate(response.json()['data']):
            item = {}
            item['rank'] = i+j+1
            item['artist'] = t['artist']['name']
            item['album'] = t['album']['title']
            item['track'] = t['title']
            item['popularity'] = t['rank']
            item['duration_ms'] = t['duration']*1000
            data.append(item)
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Convert the list of dictionaries to a Pandas DataFrame
deezer_data = pd.DataFrame(data)

# Write dataframe to Parquet file
pq.write_table(pa.Table.from_pandas(deezer_data), 'deezer_data.parquet')

# Load dataframe from Parquet file
deezer_data = pq.read_table('deezer_data.parquet').to_pandas()

# Save data to Parquet file
pq.write_table(pa.Table.from_pandas(deezer_data), 'deezer_data.parquet')

###########################################################################################

# Load both dataframes from Parquet files
spotify_data = load_dataframe_from_parquet('spotify_data.parquet')
deezer_data = load_dataframe_from_parquet('deezer_data.parquet')

# Concatenate dataframes vertically
combined_data = pd.concat([spotify_data, deezer_data], axis=0)

# Save combined dataframe to a new Parquet file
save_dataframe_to_parquet(combined_data, 'combined_data.parquet')