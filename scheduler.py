from apscheduler.schedulers.background import BackgroundScheduler
from config import PARSER_NEWS_COUNT, PARSER_INTERVAL_SECONDS


def load_news():
    news = get_news()
    print('success task')


def get_news():
    return []


def init():
    background_scheduler = BackgroundScheduler(daemon=True)
    background_scheduler.add_job(load_news, 'interval', seconds=PARSER_INTERVAL_SECONDS)
    background_scheduler.start()
