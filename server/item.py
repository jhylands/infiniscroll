from neo.main import FeedItem
# The idea behind this class is that it represents an item which will be leaded into the feed


class Item:
    @staticmethod
    def from_feed_item(item: FeedItem):
        title = item.get("title").value
        description = item.get("summary").value
        link = item.get("link").value
        thumbnail = item.get("media_thumbnail").get("url").value
        item = Item(title)
        item.link = link
        item.content = "<img src=\"{}\" /><p>{}</p>".format(thumbnail, description[:1000])
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
