import feedparser
# The purpose of this module is simply to get a feed
# So at the moment this is basically the requests get call


def parse(url):
    return feedparser.parse(url).entries
