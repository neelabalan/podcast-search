import logging
import uuid
import json
import os
import sys
from xml.etree import ElementTree

import feedparser
import meilisearch

URL = 'http://meilisearch:7700'

def extract_url_from_opml(filename='podcasts.opml'):
	urls = list()
	with open(filename, "rt") as file:
		tree = ElementTree.parse(file)
	for node in tree.findall(".//outline"):
		url = node.attrib.get("xmlUrl")
		if url:
			urls.append(url)
	print("urls extracted from {} - {}".format(filename, urls))
	return urls


def get_feeds(urls):
	feeds = list()
	for url in urls:
		feed = feedparser.parse(url)
		if feed.status == 200:
			feeds.append(feedparser.parse(url))
			print("url parsed - {}".format(url))
		else:
			print(
				"status - {} while parsing url {}".format(feed.status, url)
			)
	return feeds

def get_channel_title(feed):
	return feed.get("channel").get("title")

def construct_episodes(feeds):
	episodes = list()
	for feed in feeds:
		entries = feed.entries
		title = get_channel_title(feed)
		for entry in entries:
			firstlink = entry.get("links")[0]
			secondlink = (
				entry.get("links")[1] if len(entry.get("links")) > 1 else dict()
			)
			textlink, audiolink = (
				(firstlink.get("href"), secondlink.get("href"))
				if "text" in firstlink.get("type")
				else (secondlink.get("href"), firstlink.get("href"))
			)
			image = entry.get('image')
			image_url = 'https://cdn.pixabay.com/photo/2017/08/21/12/16/podcast-2665179_960_720.png'
			if image:
				image_url = image.get('url') or image.get('href')
			episodes.append(
				dict(
					id=str(uuid.uuid4()),
					podcast=title,
					title=entry.title.replace("\u00A0", " "),
					subtitle=entry.get("subtitle"),
					published=entry.get("published"),
					audiolink=audiolink,
					link=textlink,
					poster=image_url,
				)
			)
		print("dict construction complete for {}".format(title))
	return episodes


def run(filename):
	client = meilisearch.Client(URL)
	urls = extract_url_from_opml(filename)
	feeds = get_feeds(urls) # feeds: Dict
	documents = construct_episodes(feeds) 
	json.dump(documents, open('documents.json', 'w'))
	client.index('podcasts').add_documents(documents)


if __name__ == '__main__':
	args = sys.argv
	filename = args[1] if len(args) > 0 else None
	if not filename: 
		sys.exit('no user provided')
	if not os.path.exists(filename):
		sys.exit('path does not exist')
	run(filename)	