# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: config.py
# time: 9:57 上午

import os
import pathlib


class Config:

    def __init__(self):
        self.PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
        self.DATA_DIR = os.path.join(self.PROJECT_DIR, 'data')
        self.MOVIE_DIR = os.path.join(self.DATA_DIR, 'movies')
        pathlib.Path(self.DATA_DIR).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.MOVIE_DIR).mkdir(parents=True, exist_ok=True)


conf = Config()


if __name__ == "__main__":
    pass
