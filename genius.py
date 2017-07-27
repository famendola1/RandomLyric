import requests
from bs4 import BeautifulSoup
import re
import random

base_url = "http://api.genius.com"
headers = {
    'Authorization': 'Bearer zOfYhZ1H5ecBknpmCJiLg-0gmEXvHhGFtnUMyuds9z8JRyDTU_7vxcagoy5e1oMv'}

song_title = input("Song: ")
artist_name = input("By: ")


def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    # gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    # remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    # at least Genius is nice and has a tag called 'lyrics'!
    # updated css where the lyrics are based in HTML
    lyrics = html.find("div", class_="lyrics").get_text()
    return lyrics

if __name__ == "__main__":
    search_url = base_url + "/search"
    query = song_title + " " + artist_name
    payload = {'q': query}
    response = requests.get(search_url, params=payload, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower():
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        song_lyrics = lyrics_from_song_api_path(song_api_path)
        line = re.compile(r'^[^\W].+$', flags=re.MULTILINE)
        all_lines = line.findall(song_lyrics)
        all_lines = list(map(lambda x: x.strip(), all_lines))
        used_lyrics = set()
        while True:
            lyric = ""
            while True:
                index = random.randint(0, len(all_lines) - 1)
                lyric = all_lines[index]
                if lyric not in used_lyrics:
                    used_lyrics.add(lyric)
                    break
            print(lyric)
            new_lyric = input("Another Lyric? (y/n): ")
            if new_lyric == "n":
                break
    else:
        print("Sorry, song not found :(")
