from worker.tasks import load_feed
from neo.functions import get_feeds, add_feed_item
from time import sleep


def gather_update():
    # should maybe be using a task set for this
    results = [(load_feed.delay(feed.url), feed) for feed in get_feeds()]
    while not results[0][0].ready():
        pass
    for result_tuple in results:
        result, feed = result_tuple
        if result.ready():
            articles = result.get()
            for article in articles:
                add_feed_item(feed, article)
            del result_tuple


if __name__ == "__main__":
    gather_update()
