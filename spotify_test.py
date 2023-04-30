import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

cid='651c908112b04c008f843b0fa3475186'
secret='d458245047e54d22bbcc7af4ba51031f'
#export SPOTIPY_REDIRECT_URI=http://localhost:8080/

birdy_uri = 'spotify:artist:4tZwfgrHOc3mvqYlEYSvVi'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))

#name = 'Daft Punk'
#results1 = spotify.artist_top_tracks(birdy_uri, country= 'US')
#
#for track in results1['tracks'][:10]:
#    print('track  : ' + track['name'])
#    print('audio    : ' + track['preview_url'])
#    print('album: ' + track['album']['name'])
#    print()

#results = spotify.search(q='artist:' + name, type='artist')
#items = results['artists']['items']
#if len(items) > 0:
#    artist = items[0]
#    print(artist['name'], artist['images'][0]['url'])

#export SPOTIPY_CLIENT_ID=651c908112b04c008f843b0fa3475186
#export SPOTIPY_CLIENT_SECRET=d458245047e54d22bbcc7af4ba51031f
#export SPOTIPY_REDIRECT_URI=http://localhost:8080/

#playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
#playlist_URI = playlist_link.split("/")[-1].split("?")[0]
#track_uris = [x["track"]["uri"] for x in spotify.playlist_tracks(playlist_URI)["items"]]
#
#
#for track in spotify.playlist_tracks(playlist_URI)["items"]:
#    #URI
#    track_uri = track["track"]["uri"]
#    
#    #Track name
#    track_name = track["track"]["name"]
#    
#    #Main Artist
#    artist_uri = track["track"]["artists"][0]["uri"]
#    artist_info = spotify.artist(artist_uri)
#    
#    #Name, popularity, genre
#    artist_name = track["track"]["artists"][0]["name"]
#    artist_pop = artist_info["popularity"]
#    artist_genres = artist_info["genres"]
#    
#    #Album
#    album = track["track"]["album"]["name"]
#    
#    #Popularity of the track
#    track_pop = track["track"]["popularity"]
#    
#    z=spotify.audio_features(track_uri)[0]


#artist_name = []
#track_name = []
#popularity = []
#track_id = []
#danceability = []
#energy = []
#duration_ms = []
#track_number = []
#available_markets =[]
#for i in range(0,100):
#    track_results = spotify.search(q='year:2023', type='track', limit=50,offset=i)
#    for i, t in enumerate(track_results['tracks']['items']):
#        artist_name.append(t['artists'][0]['name'])
#        track_name.append(t['name'])
#        track_id.append(t['id'])
#        popularity.append(t['popularity'])
#        duration_ms.append(t['duration_ms'])
#        track_number.append(t['track_number'])
#        available_markets.append(t['available_markets'])
#
#
#track_dataframe = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_id' : track_id, 'popularity' : popularity, 'duration_ms' : duration_ms, 'track_number' : track_number, 'available_markets' : available_markets})
#print(track_dataframe)
#
#track_dataframe.to_csv(r'\\wsl$\Ubuntu\home\mattnew\airflow\dags\data.csv', index=None)

results = spotify.search(q='year:2022', type='track', limit=50)
tracks = results['tracks']['items']

data = []
for i in range(0, 500, 50):
    track_results = spotify.search(q='year:2018', type='track', limit=50, offset=i)
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

df = pd.DataFrame(data)

#df.to_parquet('df.parquet.gzip',compression='gzip')  
# pd.read_parquet('df.parquet.gzip') 


print(df)