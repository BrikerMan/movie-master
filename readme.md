# Movie Master
## Mini movie search / recommend example project

## Prepare Data

Apply for API KEY from [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api) .

```bash
export API_KEY=xxxxx
scrapy crawl movies
```

## Index Data

```bash
python jina_app.py -t index -n 10000
```

## Query in Terminal

```bash
python jina_app.py -t query
```

## Query in Web-Page
