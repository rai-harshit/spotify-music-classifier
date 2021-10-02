import spotipy
import spotipy.oauth2 as oauth2

def generate_token():
    """ Generate the token. Please respect these credentials :) """
    credentials = oauth2.SpotifyClientCredentials(
        client_id='a5282b3f2be24fa2968557e40208260c',
        client_secret='109c7d644fb44b06836db8e0835711b9')
    token = credentials.get_access_token()
    return token


def write_tracks(text_file, tracks):
    with open(text_file, 'a') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    song_id = track['external_urls']['spotify'].split("/")[-1]
                    artist = track['artists'][0]['name']
                    track_url = song_id + "," + track['name'] + "," + artist + "," + str(track['popularity'])
                    #print(track_url)
                    file_out.write(track_url + '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username, playlist_id):
    results = spotify.user_playlist(username, playlist_id,
                                    fields='tracks,next,name')
    text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(
            results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)


token = generate_token()
spotify = spotipy.Spotify(auth=token)

# example playlist
write_playlist('spotify', '37i9dQZF1E36nJEz3hwAAY')