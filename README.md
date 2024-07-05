# scrape-song-lyrics-from-paroles
A Python script to scrape song lyrics from paroles.net for a list of artists. It fetches lyrics, saves them in individual text files, and handles pagination to ensure all lyrics are downloaded.

# Lyrics Scraper
A Python script to scrape and save song lyrics from paroles.net for a list of artists. The script fetches lyrics, saves them in individual text files, and handles pagination to ensure all lyrics are downloaded.

# Features
Scrapes lyrics for a list of artists provided in artists.txt.
Saves each song's lyrics in a separate text file.
Handles pagination to scrape all available songs for each artist.
Ensures duplicate pages are not processed.

# Requirements
Python 3.x
requests
beautifulsoup4
tqdm
