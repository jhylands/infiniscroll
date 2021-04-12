from item import Item
from typing import List
from neo.functions import get_user


class ItemManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_node = get_user(user_id)

    def get_feed_sources(self):
        pass

    def get_items(self, no_items):
        # type: (int)->List[Item]

        subscriptions = self.user_node.subscribed_to
        for feed in subscriptions:
            for item in feed.items:
                title = item.get("title")
                if title:
                    the_title = title.get("innerHTML").value
                    print("Title:", the_title)
                    yield Item(the_title)
                else:
                    print("no title found for item")
