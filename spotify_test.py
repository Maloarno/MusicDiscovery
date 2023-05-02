import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import pyarrow.parquet as pq

cid='651c908112b04c008f843b0fa3475186'
secret='d458245047e54d22bbcc7af4ba51031f'

birdy_uri = 'spotify:artist:4tZwfgrHOc3mvqYlEYSvVi'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))

def fetch_top_tracks(year, limit=50):
    data = []
    for i in range(0, limit, 50):
        track_results = spotify.search(q=f'year:{year}', type='track', limit=50, offset=i)
        for j, t in enumerate(track_results['tracks']['items']):
            item = {}
            item['rank'] = i+j+1
            item['artist'] = t['artists'][0]['name']
            item['album'] = t['album']['name']
            item['track'] = t['name']
            item['danceability'] = spotify.audio_features(t['id'])[0]['danceability']
            item['loudness'] = spotify.audio_features(t['id'])[0]['loudness']
            item['popularity'] = t['popularity']
            item['available_markets'] = len(t['available_markets'])
            item['duration_ms'] = t['duration_ms']
            item['energy'] = spotify.audio_features(t['id'])[0]['energy']
            item['key'] = spotify.audio_features(t['id'])[0]['key']
            item['mode'] = spotify.audio_features(t['id'])[0]['mode']
            item['speechiness'] = spotify.audio_features(t['id'])[0]['speechiness']
            item['acousticness'] = spotify.audio_features(t['id'])[0]['acousticness']
            item['instrumentalness'] = spotify.audio_features(t['id'])[0]['instrumentalness']
            item['liveness'] = spotify.audio_features(t['id'])[0]['liveness']
            item['valence'] = spotify.audio_features(t['id'])[0]['valence']
            item['platform'] = 'Spotify'
            data.append(item)
    return pd.DataFrame(data)

def sva_to_parquet(data, filename):
    df = data
    pq.write_table(pa.Table.from_pandas(df), filename)

def load_from_parquet(filename):

    return pq.read_table(filename).to_pandas()


data = fetch_top_tracks(2023,50)

