FROM python:3.8-slim-buster
WORKDIR /app
RUN pip3 install feedparser meilisearch
COPY . .
CMD [ "python3", "fetch_and_load_documents.py" , "podcasts.opml"]