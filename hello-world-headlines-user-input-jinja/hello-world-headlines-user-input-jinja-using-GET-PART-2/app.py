"""
script name   : app.py
Functionality : Simple hello world flask application using GET method
Created on    : 23 SEP 2018
"""
__author__ = 'Ganesh'

# Global Imports
from flask import Flask, render_template, request
import feedparser
import json
import urllib2
import urllib

# Global variable
BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}'\
              '&units=metric&appid=<open_weather_map_your_api_key_here>'
DEFAULTS = {'publication':'bbc',
            'city': 'London,UK'}


app = Flask(__name__)


@app.route("/")
def home():
    publication = request.args.get('publication')                               # Get customized headlines, based on user input or default
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')                                             # Get customized weather based on user input or default
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html",
                           articles=articles,
                           weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    """
    We use urllib.quote() on the query variable, as URLs cannot have spaces in
    them, but the names of the cities that we want to retrieve weather for may
    contain spaces. The quote() function handles this for us by, for example,
    translating a space to "%20", which is how spaces are represented in URLs.
    """
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        weather = {'description': parsed['weather'][0]['description'],
                   'temperature': parsed['main']['temp'],
                   'city': parsed['name'],
                   'country': parsed['sys']['country']
     }
    return weather


if __name__ == '__main__':
    app.run(port=5000, debug=True)


