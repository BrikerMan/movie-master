# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: api.py
# time: 4:01 下午

import glob
import json
import os
from typing import List
from operator import itemgetter

from fastapi import FastAPI
from pydantic import BaseModel

from config import conf
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

movie_map = {}

for movie_file in glob.glob(os.path.join(conf.MOVIE_DIR, '*.json')):
    with open(movie_file, 'r') as f:
        item = json.load(f)
        data = {
            'id': item['id'],
            'title': item['title'],
            'tag_line': item['tagline'],
            'popularity': item['popularity'],
            'poster': item['poster_path']
        }
        movie_map[item['id']] = data


class MovieItem(BaseModel):
    id: int
    title: str
    tag_line: str
    popularity: float
    poster: str = None


@app.get("/movies", response_model=List[MovieItem])
async def search_movie_by_name(movie_name: str):
    t_movies = []
    if movie_name:
        for item in movie_map.values():
            if movie_name in item['title'].lower():
                t_movies.append(item)
        t_movies = sorted(t_movies, key=itemgetter('popularity'), reverse=True)
    return t_movies


@app.get("/movies/{movie_id}", response_model=MovieItem)
async def read_movie_detail(movie_id: int):
    return movie_map[movie_id]


if __name__ == "__main__":
    pass
