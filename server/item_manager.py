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
                try:
                    yield Item.from_feed_item(item)
                except Exception as e:
                    print(e)
