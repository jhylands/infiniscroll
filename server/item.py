from neo.main import FeedItem
from typing import List, Optional

# The idea behind this class is that it represents an item which will be leaded into the feed


class Item:

    @staticmethod
    def from_feed_item(item: FeedItem):
        data = item.get_properties(["title", "summary", "link"])
        title = data["title"]
        description = data["summary"]
        link = data["link"]
        thumbnail = None #Item.get_property(item, ["media_thumbnail", "url"])
        item = Item(title)
        item.link = link
        if thumbnail:
            item.content += '<img src="{}" />'.format(thumbnail)
        if description:
            item.content += "<p>{}</p>".format(description[:1000])
        return item

    def __init__(self, title):
        # the item at least needs a title, right?
        self.title = title
        self.link = None
        self.content = ""

    def set_content(self, content):
        self.content = content

    def to_jsonable(self):
        return {"title": self.title, "link": self.link, "description": self.content}
