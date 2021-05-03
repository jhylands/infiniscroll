from item import Item
from typing import List, Generator
from neo.functions import get_user
from neo.main import Feed, FeedItem


class ItemManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_node = get_user(user_id)

    def get_feed_sources(self):
        pass

    def get_items(self, no_items):
        # type: (int)->Generator[Item]

        subscriptions: List[Feed] = self.user_node.subscribed_to
        acc = 0
        items = (item for feed in subscriptions for item in feed.items)
        for item in items:
            acc += 1
            print(item)
            yield Item.from_feed_item(item)
            if acc >= no_items:
                break
"""
MATCH 
    (u:User)-[:SUBSCRIBED]->(f:Feed),
    (i:FeedItem)-[s:SOURCE]->(f:Feed),
    (a:FeedItem)->[:PROPERTY*..4]->(i:FeedItem)
WHERE
    a.attribute IN ["title", "link", "summary"] AND
    u.id = $user_id
ORDER BY s.date DESC
LIMIT 20
"""
