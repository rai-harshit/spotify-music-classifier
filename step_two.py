import argparse
import pprint
import sys
import os
import subprocess
import json
import spotipy
import spotipy.util as util
import pandas as pd
import time
from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manager = SpotifyClientCredentials(client_id='a5282b3f2be24fa2968557e40208260c', client_secret='109c7d644fb44b06836db8e0835711b9')


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print (" %d %s %s" % (i, track['artists'][0]['name'],track['name']))

def get_track_features(track_id,sp):
    if track_id is None:
        return None
    else:
        features = sp.audio_features([track_id])
    return features

def get_features(tracks,sp):
    tracks_with_features=[]
    for track in tracks:
        features = get_track_features(track['id'],sp)
        if not features:
            print("passing track %s" % track['name'])
            pass
        else:
            f = features[0]
            print(track['name'])
            tracks_with_features.append(dict(
                                            name=track['name'],
                                            artist=track['artist'],
                                            id=track['id'],
                                            popularity=track['popularity'],
                                            danceability=f['danceability'],
                                            key=f['key'],
                                            mode=f['mode'],
                                            instrumentalness=f['instrumentalness'],
                                            duration=f['duration_ms'],
                                            time_signature=f['time_signature'],
                                            energy=f['energy'],
                                            loudness=f['loudness'],
                                            speechiness=f['speechiness'],
                                            acousticness=f['acousticness'],
                                            tempo=f['tempo'],
                                            liveness=f['liveness'],
                                            valence=f['valence']
                                            ))

    # print(tracks_with_features[0])
    return tracks_with_features

def get_tracks_from_playlists(username, sp):
    playlists = sp.user_playlists(username)
    trackList = []
    for playlist in playlists['items']:
        #if playlist['owner']['id'] == username:
        print (playlist['name'],' no. of tracks: ',playlist['tracks']['total'])
        #results = sp.user_playlist(username, playlist['id'],fields="tracks,next")
        results = sp.playlist(playlist['id'],fields="tracks,next")
        tracks = results['tracks']
        for i, item in enumerate(tracks['items']):
            if item['track'] is None:
                continue
            track = item['track']
            trackList.append(dict(name=track['name'], id=track['id'], artist=track['artists'][0]['name']))

    # print(trackList[0])
    return trackList

def write_to_csv(track_features):
    df = pd.DataFrame(track_features)
    df.drop_duplicates(subset=['name','artist'])
    print ('Total tracks in data set', len(df))
    df.to_csv('mySongsDataset.csv',index=False)

def main(username):
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    #print ("Getting user tracks from playlists")
    #tracks = get_tracks_from_playlists(username, sp)
    tracks = []
    with open("Best Hindi & Bollywood Playlist on Spotify.txt","r") as fp:
        lines = fp.readlines()
        for line in lines:
            rawData = line.split(",")
            dataDict = {
                "id" : rawData[0],
                "name": rawData[1],
                "artist": rawData[2],
                "popularity": rawData[3]
            }
            tracks.append(dataDict)
    print(len(tracks))
    print ("Getting track audio features")
    tracks_with_features = get_features(tracks,sp)
    print ("Storing into csv")
    write_to_csv(tracks_with_features)


if __name__ == '__main__':
    print ('Starting...')
    parser = argparse.ArgumentParser(description='this sript will grab user playlists')
    parser.add_argument('--username', help='username')
    args = parser.parse_args()
    main(args.username)
