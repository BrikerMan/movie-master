__copyright__ = "Copyright (c) 2020 Jina AI Limited. All rights reserved."
__license__ = "Apache-2.0"

import glob
import json
import os
import random
import string

import click
from jina.flow import Flow

from config import conf

RANDOM_SEED = 10  # 5
os.environ['REPLICAS'] = str(1)
os.environ['SHARDS'] = str(1)
os.environ['TMP_WORKSPACE'] = os.path.join(conf.DATA_DIR, 'workdir')


class DataReader:
    @classmethod
    def read(cls, count: int):
        movie_files = glob.glob(os.path.join(conf.MOVIE_DIR, '*.json'))
        movie_files = movie_files[:count]
        for movie_path in movie_files:
            item = json.load(open(movie_path, 'r'))
            text = f"{item['id']}: {item['title']} | "
            text += ' | '.join([genre['name'] for genre in item['genres']])
            text += f" || {item['overview']}"
            yield text.lower().encode('utf8')


def print_topk(resp, word):
    for d in resp.search.docs:
        print(f'Ta-Dah🔮, here are what we found for: {word}')
        for idx, kk in enumerate(d.topk_results):
            score = kk.score.value
            if score <= 0.0:
                continue
            print('{:>2d}:({:f}):{}'.format(
                idx, score, kk.match_doc.buffer.decode()))


def read_query_data(text):
    yield '{}'.format(text).encode('utf8')


@click.command()
@click.option('--task', '-t')
@click.option('--num_docs', '-n', default=50)
@click.option('--top_k', '-k', default=5)
def main(task, num_docs, top_k):
    if task == 'index':
        flow = Flow().load_config('flow-index.yml')
        with flow.build() as fl:
            fl.index(buffer=DataReader.read(num_docs), batch_size=16)
    elif task == 'query':
        flow = Flow().load_config('flow-query.yml')
        with flow.build() as fl:
            while True:
                text = input('word definition: ')
                if not text:
                    break
                ppr = lambda x: print_topk(x, text)
                fl.search(read_query_data(text), callback=ppr, topk=top_k)
    else:
        raise NotImplementedError(
            f'unknown task: {task}. A valid task is either `index` or `query`.')


if __name__ == '__main__':
    main()
