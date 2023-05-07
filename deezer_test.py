import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Set the API endpoint URL and parameters
api_url = 'https://api.deezer.com/search'
api_params = {
    'q': 'year:2018',
    'type': 'track',
    'limit': 50,
}

# Set the headers to include your API key
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
pq.write_table(pa.Table.from_pandas(deezer_data), 'top_500_tracks_deezer.parquet')

# Load dataframe from Parquet file
deezer_data = pq.read_table('top_500_tracks_deezer.parquet').to_pandas()

# Save data to Parquet file
pq.write_table(pa.Table.from_pandas(deezer_data), 'deezer_data.parquet')
