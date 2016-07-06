import requests
import csv

AUTH_TOKEN = "BQBJYh1JuJ5N9uHi-BWhTdiottv_ZD213iC-PLAJzchYA36MY4qBWS0k4dTsR7KBxnXFCwrQ6jrvq_mPMpRWiypcb4lJmM0BtMDUCWPxsZxjteOzs3EoV30oHMNRpxJroQNFaG8FxLPXg7anjr-RN23WmsthjdfHyeMT4yxSLsDN54cSKxez1C3vlwOPMqAhKQ3zP__4RJVf"

def get_tracks_from_playlist(user, playlist, limit=100, offset=0):
    if limit <= 100:
        endpoint = "https://api.spotify.com/v1/users/%s/playlists/%s/tracks" % (user, playlist)
        params = {
            "fields": "items(track(id))",
            "offset": offset,
            "limit": 100
        }
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + AUTH_TOKEN
        }
        r = requests.get(endpoint, params, headers=headers)
        data = r.json()

        return [t["track"]["id"] for t in data["items"]]
    else:
        head = get_tracks_from_playlist(user,playlist,offset=offset)
        tail = get_tracks_from_playlist(user,playlist,limit=limit-100, offset=offset+100)

        return head + tail

def get_attributes_from_tracks(tracks):
    if len(tracks) <= 100:
        endpoint = "https://api.spotify.com/v1/audio-features/"
        params = {
            "ids": ",".join(tracks)
        }
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + AUTH_TOKEN
        }
        r = requests.get(endpoint, params, headers=headers)
        data = r.json()

        return [f for f in data["audio_features"]]
    else:
        head = get_attributes_from_tracks(tracks[:100])
        tail = get_attributes_from_tracks(tracks[100:])

        return head + tail

def get_names_from_tracks(tracks):
    if len(tracks) <= 50:
        endpoint = "https://api.spotify.com/v1/tracks/"
        params = {
            "ids": ",".join(tracks)
        }
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + AUTH_TOKEN
        }
        r = requests.get(endpoint, params, headers=headers)
        data = r.json()

        return [t["name"] for t in data["tracks"]]
    else:
        head = get_names_from_tracks(tracks[:50])
        tail = get_names_from_tracks(tracks[50:])

        return head + tail


if __name__ == "__main__":
    tracks = get_tracks_from_playlist("worldwaffle", "7I0DQkqDHD8bOuUMj6QQej", limit=500)
    track_attributes = get_attributes_from_tracks(tracks)
    track_names = get_names_from_tracks(tracks)

    with open("data/spotify.dat", "wb") as f:
        writer = csv.writer(f)
        header = ["id","name","energy","liveness","tempo","speechiness","acousticness","instrumentalness","time_signature","danceability","key","loudness","valence"]
        writer.writerow(header)
        for i,attr in enumerate(track_attributes):
            computed = [attr[k] for k in header[2:]]
            t_id = unicode(tracks[i]).encode("utf-8")
            t_name = unicode(track_names[i]).encode("utf-8")
            writer.writerow([t_id] + [t_name] + computed)