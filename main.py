import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Extract 100 songs from the billboard chart -------------------------------------------------
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

song_list = soup.find_all(name="h3", id="title-of-a-story")

title_parser = [song.string for song in song_list]
converted_list = []
redundant_items = ["Songwriter(s):", "Producer(s):", "Imprint/Promotion Label:", "Gains in Weekly Performance", "Additional Awards", "Songwriter(s): ", " Imprint/Promotion Label:", " Songwriter(s):"]

for title in title_parser:
    if not title is None:
        parsed_title = title.text.strip('\n')
    if parsed_title not in redundant_items:
        converted_list.append(parsed_title)
    else:
        pass

song_names = converted_list[0:100]
print(song_names)
# End -----------------------------------------------------------

CLIENT_ID='a18f36ec40c44b12981549abdbec291c'
CLIENT_SECRET='b0e68770c8ed4c55ba31dcc0c4a580b8'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)