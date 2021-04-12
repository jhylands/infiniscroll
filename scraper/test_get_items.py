from scraper.get_items import get_feed, parse

def test_everything():
    items = parse(get_feed("http://feeds.bbci.co.uk/news/rss.xml"))
    print(items)
    assert len(items)==10
    items = parse(get_feed("https://xkcd.com/atom.xml"))
    print(items)
    assert len(items)==4
