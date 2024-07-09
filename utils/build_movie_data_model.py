
import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='/Users/josephgonzalez/dev/movie-insights/.env')
from utils import build_url
import time

# Set the path, scheme, netloc, and query parameters for the request.
PATH = "3/discover/movie"
SCHEME = 'https'
NETLOC = 'api.themoviedb.org'

# Set the headers for the request.
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('TMDB_API_ACCESS_TOKEN')}"
}

# Set initial query parameters. Page 1 is the first page of results.
params = {
    "include_adult": "false",
    "include_video": "false",
    "language": "en-US",
    "sort_by": "popularity.desc",
    "with_origin_country": "US",
    "with_runtime.gte": "60",
}

movies_df = pd.DataFrame()
for year in range(2024, 2025):
    page = 101
    max_page = 168
    time.sleep(1)
    while page <= max_page:
        params['page'] = str(page)
        params['year'] = str(year)
        url = build_url(PATH, SCHEME, NETLOC, params)
        # Get the response. If error, try again.
        failed = True
        attempts = 0
        while failed and attempts < 5:
            try:
                response = requests.get(url, headers=headers)
                failed = False  
            except requests.exceptions.Timeout:
                time.sleep(120)
                attempts += 1
                if attempts == 5:
                    print('Failed to retrieve data after 5 attempts.')
                    print(page)
        if page == 1:
            max_page = response.json()['total_pages']
        movies_temp_df = pd.DataFrame(response.json()['results'])
        movies_temp_df['page'] = page
        movies_temp_df['year'] = year
        movies_df = pd.concat([movies_df, movies_temp_df], ignore_index=True)
        if page % 50 == 0:
            print(f'page {page} of {max_page}, {response.status_code}')
            movies_df.to_pickle(f'data/tmdb_movies.pkl')
        page += 1
        time.sleep(0.05)

movies_df.to_pickle(f'data/tmdb_movies.pkl')