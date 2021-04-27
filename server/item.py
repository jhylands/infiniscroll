from neo.main import FeedItem
from typing import List, Optional

# The idea behind this class is that it represents an item which will be leaded into the feed


class Item:
    @staticmethod
    def get_property(item: FeedItem, property_list: List[str]) -> Optional[str]:
        inter_item = item
        for p in property_list:
            inter_item = inter_item.get(p)
            if inter_item is None:
                return None
        return inter_item.value

    @staticmethod
    def from_feed_item(item: FeedItem):
        title = Item.get_property(item, ["title"])
        description = Item.get_property(item, ["summary"])
        link = Item.get_property(item, ["link"])
        thumbnail = Item.get_property(item, ["media_thumbnail", "url"])
        item = Item(title)
        item.link = link
        if description:
            item.content = '<img src="{}" /><p>{}</p>'.format(thumbnail, description[:1000])
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
