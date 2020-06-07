# encoding: utf-8

# author: BrikerMan
# contact: eliyar917@gmail.com
# blog: https://eliyar.biz

# file: jina_app.py
# time: 10:00 上午

import glob
import json
import os

import click
from jina.flow import Flow

from config import conf


def read_query_data(text):
    yield '{}'.format(text).encode('utf8')


class JinaApp:
    def __init__(self, workspace: str):
        self.workspace = workspace
        os.environ['TMP_WORKSPACE'] = workspace

    def read_data(self, count: int):
        movie_files = glob.glob(os.path.join(conf.MOVIE_DIR, '*.json'))
        movie_files = movie_files[:count]
        for movie_path in movie_files:
            item = json.load(open(movie_path, 'r'))
            text = f"{item['id']}: {item['title']} | "
            text += ' | '.join([genre['name'] for genre in item['genres']])
            text += f" || {item['overview']}"
            yield text.lower().encode('utf8')

    def print_top_k(self, resp, query: str):
        for d in resp.search.docs:
            print(f'Ta-Dah🔮, here are what we found for: {query}')
            for idx, kk in enumerate(d.topk_results):
                score = kk.score.value
                if score <= 0.0:
                    continue
                text = kk.match_doc.buffer.decode()
                movie_id = text.split(': ')[0]
                movie_name = text.split(': ')[1].split(' | ')[0]
                movie_summary = text.split('|| ')[1]
                print(f"Score   : {score}")
                print(f"Movie   : {movie_id} - {movie_name}")
                print(f"URL     : https://www.themoviedb.org/movie/{movie_id}")
                print(f"Summary : {movie_summary}")
                print('-' * 70)
                print()

    def index(self, num_docs: int, batch_size: int):
        flow = Flow().load_config('flow-index.yml')
        with flow.build() as fl:
            fl.index(buffer=self.read_data(num_docs), batch_size=batch_size)

    def query(self, top_k: int):
        flow = Flow().load_config('flow-query.yml')
        with flow.build() as fl:
            while True:
                text = input('movie plot: ')
                if not text:
                    break
                text = text.replace('movie plot: ', '').lower()
                ppr = lambda x: self.print_top_k(x, text)
                fl.search(read_query_data(text), output_fn=ppr, topk=top_k)


@click.command()
@click.option('--task', '-t')
@click.option('--workspace', '-ws', default=None)
@click.option('--num_docs', '-n', default=50)
@click.option('--top_k', '-k', default=5)
@click.option('--batch_size', default=32)
def main(task: str, workspace: str, num_docs: int, top_k: int, batch_size: int):
    os.environ['REPLICAS'] = str(1)
    os.environ['SHARDS'] = str(1)

    if workspace is None:
        workspace = os.path.join(conf.DATA_DIR, 'workspace')

    j = JinaApp(workspace)
    if task == 'index':
        j.index(num_docs, batch_size=batch_size)
    elif task == 'query':
        j.query(top_k)
    else:
        raise NotImplementedError(
            f'unknown task: {task}. A valid task is either `index` or `query`.')


if __name__ == "__main__":
    main()
