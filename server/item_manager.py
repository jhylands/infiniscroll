from item import Item
from typing import List


class ItemManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_feed_sources(self):
        pass

    def get_items(self, no_items):
        # type: (int)->List[Item]
        return []
