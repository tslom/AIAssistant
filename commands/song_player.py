import os
import spotipy
from dotenv import load_dotenv
from spotipy import SpotifyOAuth
from utils.utils import nlp

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = "user-modify-playback-state user-read-playback-state user-read-currently-playing"
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Authenticate with Spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE,
                              redirect_uri=REDIRECT_URI))


def play_song_on_spotify(song_data):
    """
    Searches for a song on Spotify by name and artist, and starts playing it on an active device.

    This function communicates with the Spotify API to find the song based on the given song name
    and artist, and plays it on the user's active device if available.

    Args:
        song_data (dict): A dictionary containing the song's name under the key 'song' and the artist's name under the key 'artist'.

    Returns:
        str: A message indicating the result. Either a success message with the song details or an error message.

    Raises:
        spotipy.exceptions.SpotifyException: If there is an error while interacting with the Spotify API.
        Exception: For any other errors during the process.
    """
    try:
        song_name = song_data.get("song")
        artist_name = song_data.get("artist")
        if song_name:
            song_name.strip()
        if artist_name:
            artist_name.strip()

        print(song_name, artist_name)

        # Search for the song
        results = sp.search("track:\"" + song_name + "\" artist:\"" + artist_name + "\"", 10, 0, "track")
        if results["tracks"]["items"]:
            # Get the first track's URI
            track = results["tracks"]["items"][0]
            track_uri = track["uri"]

            # Get user's active device
            devices = sp.devices()
            if devices["devices"]:
                device_id = devices["devices"][0]["id"]

                # Start playback on the active device
                sp.add_to_queue(device_id=device_id, uri=track_uri)
                sp.next_track(device_id=device_id)
                return f"Now playing {track['name']} by {track['artists'][0]['name']}."
            else:
                return "No active Spotify devices found. Please start playing Spotify on a device first."
        else:
            return "Song not found on Spotify."
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def extract_song_and_artist(text):
    """
    Extracts the song name and artist from a given text string.

    This function uses natural language processing (NLP) to identify the song name and artist
    from the user's text. It looks for proper nouns, and the word "by" to extract the relevant
    details. The text should be in the format "play [song] by [artist]" for best results.

    Args:
        text (str): The text input provided by the user, potentially containing a song and artist.

    Returns:
        dict: A dictionary with two keys: 'song' and 'artist', holding the extracted song name and artist name, respectively.
              If no artist is found, the 'artist' value will be None.
    """
    doc = nlp(text)
    proper_nouns = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "WORK_OF_ART"]]
    song_name = None
    artist_name = None
    if "by" in text:
        parts = text.split("by")
        song_name = parts[0].replace("play", "").strip()
        artist_name = parts[1].strip()
    elif proper_nouns:
        song_name = proper_nouns[0]
        artist_name = " ".join(proper_nouns[1:]) if len(proper_nouns) > 1 else None

    return {"song": song_name, "artist": artist_name}
