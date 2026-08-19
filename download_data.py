import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
import re
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
client_id = 'ad39aec7bb3646f2916cf3cc35499aad'
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# fetch albums by release year
def fetch_albums_by_year(year, limit=20):
    results = sp.search(q=f'year:{year}', type='album', limit=limit)
    albums = results['albums']['items']
    return albums

def load_formats(csv_path='formats.csv'):
    formats = []
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            formats.append((row['format'], int(row['start_yeart']), int(row['end_year'])))
    return formats

def get_format_for_year(year, formats):
    # Pick the earliest-starting format whose range covers the year,
    # so that vinyl takes priority over tape, cd over digital_download, etc.
    match = None
    for fmt, start, end in formats:
        if start <= year <= end:
            if match is None or start < match[1]:
                match = (fmt, start)
    return match[0] if match else 'pre_vinyl'

FORMATS = load_formats()

def sanitize_album_name(album_name):
    # replace invalid characters with underscore
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', album_name)
    return sanitized_name

# download album art
def download_album_art(album, year):
    album_name = sanitize_album_name(album['name'])
    album_art_url = album['images'][0]['url']  # Get the first (largest) image
    album_art_response = requests.get(album_art_url)

    # Create the 'dataset' directory if it doesn't exist
    dataset_dir = 'dataset'
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Create directory for the year if it doesn't exist
    year_dir = os.path.join(dataset_dir, str(year))  # Join 'dataset' with the year folder
    if not os.path.exists(year_dir):
        os.makedirs(year_dir)
    
    # Save image file
    file_path = os.path.join(year_dir, f'{album_name}_{str(year)}.jpg')
    with open(file_path, 'wb') as f:
        f.write(album_art_response.content)

    print(f"Downloaded {album_name} art from {str(year)}")

# Fetch the 20 most popular albums for a specific year and download the art
def collect_album_arts_by_year(start_year, end_year):
    for year in range(start_year, end_year + 1):
        print(f"Fetching albums for year {str(year)}...")
        albums = fetch_albums_by_year(year)
        for album in albums:
            download_album_art(album, year)

# Example: Collect album art from 2020 to 2025
collect_album_arts_by_year(1956, 2019)
