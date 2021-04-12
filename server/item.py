from neo.main import FeedItem
# The idea behind this class is that it represents an item which will be leaded into the feed

class Item:
    @staticmethod
    def from_feed_item(item: FeedItem):
        title = item.get("title").value
        return Item(title)

    def __init__(self, title):
        # the item at least needs a title, right?
        self.title = title

    def to_jsonable(self):
        return {"title": self.title}
