# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: movies.py
# time: 10:01 上午

import datetime
import json
import os
import zlib
from operator import itemgetter
from typing import List, Dict

import requests
import scrapy
from scrapy.http.response.text import TextResponse

from config import conf


class PopularMovies:
    def __init__(self):
        self.day = datetime.datetime.utcnow() - datetime.timedelta(days=1)

    def get_daily_file_path(self) -> str:
        """
        Get yesterday's movie ids file
        :return: movie ids file path
        """
        movie_ids_path = f"movie_ids_{self.day.strftime('%d_%m_%Y')}.json"
        full_path = os.path.join(conf.DATA_DIR, movie_ids_path)
        if os.path.exists(full_path):
            return full_path

        # Download If needs
        res = requests.get(f'http://files.tmdb.org/p/exports/{movie_ids_path}.gz')
        data = zlib.decompress(res.content, zlib.MAX_WBITS | 32)

        with open(os.path.join(conf.DATA_DIR, movie_ids_path), 'wb') as f:
            f.write(data)
        return full_path

    def get_top_k_movies(self, full_file_path: str, top_k: int) -> List[Dict]:
        """
        Get top k popular movie items from all movies
        :param full_file_path: movie ids file path
        :param top_k:
        :return:
        """
        movies = []
        with open(full_file_path, 'r') as f:
            for line in f.readlines():
                try:
                    item = json.loads(line)
                    movies.append(item)
                except:
                    pass
        sorted_movies = sorted(movies, key=itemgetter('popularity'), reverse=True)
        return sorted_movies[:top_k]

    def get_top_ids(self, top_k: int = 10000) -> List[int]:
        full_file_path = self.get_daily_file_path()
        top_movies = self.get_top_k_movies(full_file_path, top_k=top_k)
        new_top_movies = []
        for movie in top_movies:
            # If already downloaded, just pass
            if not os.path.exists(os.path.join(conf.MOVIE_DIR, f"{movie['id']}.json")):
                new_top_movies.append(movie['id'])
        return new_top_movies


class QuotesSpider(scrapy.Spider):
    name = "movies"

    def __init__(self):
        super(QuotesSpider, self).__init__()
        self.popular_movies = PopularMovies()
        self.api_key = os.environ.get('API_KEY')
        self.language = 'en-US'
        if self.api_key is None:
            raise ValueError('You need to set environment variable API_KEY before running the script.')

    def start_requests(self):
        for movie_id in self.popular_movies.get_top_ids():
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.api_key}&language={self.language}"
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['id'] = movie_id
            yield request

    def parse(self, response: TextResponse):
        movie_id = response.meta['id']
        movie_file_path = os.path.join(conf.MOVIE_DIR, f"{movie_id}.json")
        with open(movie_file_path, 'wb') as f:
            f.write(response.body)


if __name__ == "__main__":
    pass
