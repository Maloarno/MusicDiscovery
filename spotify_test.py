import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:4tZwfgrHOc3mvqYlEYSvVi'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

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

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in spotify.playlist_tracks(playlist_URI)["items"]]


for track in spotify.playlist_tracks(playlist_URI)["items"]:
    #URI
    track_uri = track["track"]["uri"]
    
    #Track name
    track_name = track["track"]["name"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = spotify.artist(artist_uri)
    
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]
    
    #Album
    album = track["track"]["album"]["name"]
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]
    
    z=spotify.audio_features(track_uri)[0]

    print(artist_info)