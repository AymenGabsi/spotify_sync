import requests

def get_liked_songs(auth_token):
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    liked_songs = []
    url = 'https://api.spotify.com/v1/me/tracks'
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        liked_songs.extend(
            {'id': item['track']['id'], 'added_at': item['added_at']} for item in data['items']
        )
        url = data['next']
    # Sort songs by added_at timestamp
    liked_songs.sort(key=lambda x: x['added_at'])
    return [song['id'] for song in liked_songs]

def add_songs_to_library(auth_token, song_ids):
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
    url = 'https://api.spotify.com/v1/me/tracks'
    for i in range(0, len(song_ids), 50):  # Spotify API allows up to 50 songs per request
        batch = song_ids[i:i+50]
        response = requests.put(url, headers=headers, json={'ids': batch})
        if response.status_code != 200:
            print(f'Error adding songs: {response.status_code}, {response.json()}')
        else:
            print(f'Successfully added {len(batch)} songs')

source_auth_token = 'source_account_auth_token'
target_auth_token = 'target_account_auth_token'

liked_songs = get_liked_songs(source_auth_token)
add_songs_to_library(target_auth_token, liked_songs)
