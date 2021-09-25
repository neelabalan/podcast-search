# podcast search 

[![recording.gif](https://i.postimg.cc/4dJPj6gB/recording.gif)](https://postimg.cc/zLcTgR3g)

____

[Meilisearch](https://github.com/meilisearch/MeiliSearch) is a search engine written in Rust, has RESTful API for interaction and it's pretty fast!
The builtin React UI is used here as such without any modification.


The podcast feed is in XML and need to be converted to JSON which the Meilisearch understands. I had to modify [podcastutil](https://github.com/neelabalan/podcastutil) a little bit here for the conversion. 

There are four podcast URLs added in the `podcasts.opml` file.
The `documents.json` file gives an idea of how the document looks like.

```xml
<outline text="feeds">
    <outline type="rss" text="good news podcast" xmlUrl="https://feeds.transistor.fm/the-good-news-podcast" />
    <outline type="rss" text="daily tech news show" xmlUrl="http://feeds.feedburner.com/DailyTechNewsShow" />
    <outline type="rss" text="tim ferris show" xmlUrl="https://rss.art19.com/tim-ferriss-show" />
    <outline type="rss" text="lex friedman" xmlUrl="https://lexfridman.com/feed/podcast/" />
</outline>
```

## How to run?

### with `docker-compose`

```bash
# clone the repo
# change directory to the folder
docker-compose build 
docker-compose up
```

### dockerless

```bash
curl -L https://install.meilisearch.com | sh

./meilisearch

# change URL in fetch_and_load_documents.py 
# from
# URL = 'http://meilisearch:7700'
# to
# URL = 'http://localhost:7700'
```
