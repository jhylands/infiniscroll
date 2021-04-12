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

        items = [subscription.items for subscription, index in zip(self.user_node.subscribed_to, range(no_items))]
        return [Item.from_feed_item(feed_item) for feed_item in items]
