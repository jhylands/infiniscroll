from py2neo import Relationship
from neo.main import graph, Feed, User, FeedItem
from typing import Optional, Iterable, Union, List
import datetime


def get_feeds() -> Iterable[Feed]:
    return Feed.match(graph).all()


def get_items(feed):
    # need to somehow relate this to the graph
    return FeedItem.match(graph)


def get_items_for_user(user_id):
    user = get_user(user_id)
    return [subscription.items for subscription in user.subscribed_to]


def get_user(user_id):
    # type:(int)->User
    return User.match(graph).where(id=user_id).first()


def add_user(user: dict) -> User:
    # need to add assurance that the user doesn't
    # already exist
    user_id = user.get("id")  # type: int
    if user := get_user(user_id):
        return user
    user_model = User()
    user_model.id = user_id
    user_model.name = user.get("name")
    user_model.email = user.get("email")
    graph.create(user_model)
    return user_model


def subscribe(user: User, feed: Feed):
    now = datetime.datetime.now()
    graph.create(Relationship(user.__node__, "SUBSCRIBED", feed.__node__, when=now))


def get_feed_from_url(url: str) -> Optional[Feed]:
    return Feed.match(graph).where("_.url='{}'".format(url)).first()


def add_feed(title: str, url: str) -> Feed:
    # Needs a gaurd against duplication
    if feed := get_feed_from_url(url):
        return feed
    feed = Feed()
    feed.title = title
    feed.url = url
    graph.create(feed)
    return feed


def add_property(parent, attribute, key=""):
    if isinstance(attribute, str):
        print("key", key)
        print("value", attribute)
        item_property = FeedItem()
        item_property.attribute = key
        item_property.value = attribute
        item_property.parent_item.add(parent)
        yield item_property
    elif isinstance(attribute, list):
        print("list")
        item_property = FeedItem()
        item_property.attribute = key
        item_property.parent_item.add(parent)
        yield item_property
        for sub_attribute in attribute:
            for item in add_property(item_property, sub_attribute):
                yield item
    elif isinstance(attribute, dict):
        print("key", key)
        item_property = FeedItem()
        item_property.attribute = key
        item_property.parent_item.add(parent)
        yield item_property
        for key, sub_attribute in attribute.items():
            for item in add_property(item_property, sub_attribute, key):
                yield item
    else:
        add_property(parent, str(attribute), key)


def extract_link(feed_item: Union[dict, List]) -> str:
    """
        So the idea here is that we do a search guided by
        the presence of keys like "link"
    match (a:FeedItem {attribute:"href"})-[:PROPERTY]-> (l:FeedItem {attribute:"link"})-[r2:PROPERTY]->(:FeedItem)-[r1:PROPERTY]->(n:FeedItem)-[r:SOURCE]->(p) return a.value
    match (a:FeedItem {attribute:"href"})-[:PROPERTY*..4]->(n:FeedItem)-[r:SOURCE]->(p) return a.value
    """
    if isinstance(feed_item, list):
        [extract_link(item) for item in feed_item]
    elif "link" in feed_item:
        if isinstance(feed_item["link"], dict):
            if "href" in feed_item["link"]:
                return feed_item["link"]["href"]
            elif "innerHTML" in feed_item["link"]:
                return feed_item["link"]["innerHTML"]
        print("Could not find link here: ", feed_item["link"])
    else:
        return False


def add_feed_item(feed_source: Feed, feed_item: dict):
    link = extract_link(feed_item)
    if link:
        results = graph.run(
            'match (a:FeedItem {attribute:"href"})-[:PROPERTY*..4]->(n:FeedItem)-[r:SOURCE]->(p) where a.value="$value"return a.value',
            value=link,
        )
        if results:
            print("values already found in the database, skipping")
            return
    feed_item_model = FeedItem()
    feed_item_model.source.add(feed_source)
    graph.create(feed_item_model)
    for property_ in add_property(feed_item_model, feed_item):
        graph.create(property_)
