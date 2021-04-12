from celery import Celery
from scraper.get_items import parse

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')


@app.task
def load_feed(url):
    # the issue here is that the feed need to be a json but that we are treating it as if it's something more.

    return parse(url)
