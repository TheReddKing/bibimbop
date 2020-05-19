import requests
from bs4 import BeautifulSoup

def fetch_musixmatch_lyrics(url):
    """
    Fetch lyrics of Korean song from Musixmatch
    """
    r = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    })
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features="html.parser")
        lyric_spans = soup.find_all("span", class_="lyrics__content__ok")
        lyrics = []
        for span in lyric_spans:
            for content in span.contents:
                lyrics += content.split("\n")
        filtered_lyrics = [line for line in lyrics if len(line) > 0]
        return filtered_lyrics
    else:
        print(f"Could not fetch {url}")

def fetch_lyrics(url):
    """
    Fetch lyrics of Korean song from URL
    """
    if "musixmatch" in url:
        return fetch_musixmatch_lyrics(url)
    else:
        raise Exception("URL website not supported")

if __name__ == "__main__":
    print(fetch_lyrics("https://www.musixmatch.com/lyrics/EXO-7/Lucky-One"))
