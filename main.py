import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import time

def fetch_page_content(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch {url}")

def extract_text_from_html(s):
    # s represent soup
    # Remove script and style elements
    for script_or_style in s(['script', 'style']):
        script_or_style.decompose()
    # Get text and strip leading/trailing spaces
    text = s.get_text(separator=' ')
    return ' '.join(text.split())

def compare_pages(s1, s2):
    text1 = extract_text_from_html(s1)
    text2 = extract_text_from_html(s2)
    
    return text1 == text2



def genarate_url(artist_name):
    name = artist_name.replace(' ', '-')
    url = "https://www.paroles.net/" + name
    return url


def scrape_lyrics(path1, soup):
    songs = soup.find_all('p', attrs={"itemprop":"name"})
    for song in songs:
        a_tag = song.find('a')
        if a_tag:
            href = a_tag.get('href')
            name = href.split('/')[-1]
            name = name.replace('paroles-', '')
            link = "https://www.paroles.net" + href
            try:
                resp = fetch_page_content(link)
                soup2 = BeautifulSoup(resp, 'html.parser')
                lyrics_div = soup2.find('div', class_="song-text")

                if lyrics_div:
                    lyrics = lyrics_div.text.strip()
                    
                    # Create the text file and save the lyrics
                    file_path = os.path.join(path1, f"{name}.txt")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(lyrics)
                    print(f"Lyrics for '{name}' saved to {file_path}")

            except Exception as e:
                print(f"Failed to fetch lyrics for {name}: {e}")

def scrape_and_save(artists):
    for artist in tqdm(artists):
        time.sleep(1)
        try:
            artist_page = genarate_url(artist)
            page=2
            response = fetch_page_content(artist_page)
            folder_name = artist_page.replace('https://www.paroles.net/', '')
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            else:
                print(f"Directory '{folder_name}' already exists")
            soup = BeautifulSoup(response, 'html.parser')
            prev_soup = soup
            scrape_lyrics(folder_name, soup)
            #for each page
            while True:
                artist_next_page = artist_page + "-" + str(page)
                response = fetch_page_content(artist_next_page)
                soup = BeautifulSoup(response, 'html.parser')
                if compare_pages(prev_soup, soup):
                    break
                else:
                    scrape_lyrics(folder_name, soup)
                    prev_soup = soup
                    i+=1

        except Exception as e:
            print("Error on artist: ", artist)



# Open the file in read mode
with open('artists.txt', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

# Strip newline characters from each line
artists = [line.strip() for line in lines]

scrape_and_save(artists)