import requests
import pandas as pd

# Set the API endpoint URL and parameters
url = 'https://api.deezer.com/search'
params = {
    'q': 'year:2018',
    'type': 'track',
    'limit': 50,
}

# Set the headers to include your API key
headers = {
    'x-rapidapi-host': 'https://developers.deezer.com/myapps/app/601084',
    'x-rapidapi-key': '3e678ee2516677d0c092634065eef4f3',
}

# Make the API requests and collect data in a list of dictionaries
data = []
for i in range(0, 500, 50):
    params['index'] = i
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        for j, t in enumerate(response.json()['data']):
            item = {}
            item['rank'] = i+j+1
            item['artist'] = t['artist']['name']
            item['album'] = t['album']['title']
            item['track'] = t['title']
          #  item['danceability'] = t['danceability']
           # item['loudness'] = t['loudness']
            item['popularity'] = t['rank']
           # item['available_markets'] = len(t['available_countries'].split(','))
            item['duration_ms'] = t['duration']*1000
           # item['energy'] = t['energy']
           # item['key'] = t['key']
           # item['mode'] = t['mode']
           # item['speechiness'] = t['speechiness']
            #item['acousticness'] = t['acousticness']
            #item['instrumentalness'] = t['instrumentalness']
            #item['liveness'] = t['liveness']
          #  item['valence'] = t['valence']
            data.append(item)
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(data)
print(df)

# Save the DataFrame to a CSV file
df.to_csv('top_500_tracks_deezer.csv', index=False)

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('top_500_tracks_deezer.csv')

# Print the first few rows of the DataFrame
print(df.head())
