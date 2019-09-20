import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask_apscheduler import APScheduler
from config import PARSER_NEWS_COUNT, PARSER_INTERVAL_SECONDS
from models import NewsModel, db

MAIN_NEWS_LINK = 'https://news.ycombinator.com/'
SELECTOR = '.storylink'


class Config(object):
    JOBS = [
        {
            'id': 'load_news',
            'func': 'scheduler:load_news',
            'args': (),
            'trigger': 'interval',
            'seconds': PARSER_INTERVAL_SECONDS
        }
    ]

    SCHEDULER_API_ENABLED = True


def load_news():
    news_dicts = parse_news()
    with db.atomic():
        NewsModel.insert_many(news_dicts).execute()


def parse_news():
    r = requests.get(MAIN_NEWS_LINK)
    soup = BeautifulSoup(r.text, 'html.parser')
    news = soup.select(SELECTOR)
    news_dicts = []
    created = datetime.utcnow().isoformat()
    count_news = min(len(news), PARSER_NEWS_COUNT)
    for one_news in news[:count_news]:
        news_dicts.append({
            'title': one_news.text,
            'url': one_news['href'] if 'href' in one_news.attrs else None,
            'created': created
        })
    return news_dicts


def init(app):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
