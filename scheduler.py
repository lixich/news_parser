import requests
from bs4 import BeautifulSoup
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from config import PARSER_NEWS_COUNT, PARSER_INTERVAL_SECONDS
from models import NewsModel, db

MAIN_NEWS_LINK = 'https://news.ycombinator.com/'
SELECTOR = '.storylink'


def load_news():
    news_dicts = get_news()
    with db.atomic():
        NewsModel.insert_many(news_dicts).execute()
        print('success insert')


def get_news():
    r = requests.get(MAIN_NEWS_LINK)
    soup = BeautifulSoup(r.text, 'html.parser')
    news = soup.select(SELECTOR)
    news_dicts = []
    created = datetime.utcnow().isoformat()
    for one_news in news:
        news_dicts.append({
            'title': one_news.text,
            'url': one_news['href'] if 'href' in one_news.attrs else None,
            'created': created
        })
    return news_dicts


def init():
    background_scheduler = BackgroundScheduler(daemon=True)
    background_scheduler.add_job(load_news, 'interval', seconds=PARSER_INTERVAL_SECONDS)
    background_scheduler.start()
