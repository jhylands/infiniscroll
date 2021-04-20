# The purpose of this module is to provide an interface that
# allows for access to the items

from py2neo import Graph
from py2neo.ogm import Model, Property, RelatedTo, RelatedFrom
import os
graph = Graph(host="bolt.timep.co.uk",  password=os.environ["neocode"])


class Feed(Model):
    name = Property("name")
    url = Property("url")

    subscribers = RelatedFrom("User", "SUBSCRIBED")
    items = RelatedFrom("FeedItem", "SOURCE")


class User(Model):
    __primarykey__ = "id"
    id = Property("id")
    name = Property("name")
    email = Property("email")

    subscribed_to = RelatedTo(Feed, "SUBSCRIBED")


class PropertyAble(Model):
    pass


class FeedItem(Model):
    attribute = Property()
    value = Property()
    source = RelatedTo(Feed, "SOURCE")
    properties = RelatedFrom("FeedItem", "PROPERTY")
    parent_item = RelatedTo("FeedItem", "PROPERTY")

    def get(self, key):
        graph = self.__ogm__.node.graph
        results = graph.run("""
match (a:FeedItem {{attribute:\"{}\"}})-[:PROPERTY*..4]->(n:FeedItem)
where ID(n)={} return a limit 1;
""".format(key, self.__primaryvalue__))
        return FeedItem.wrap(results.evaluate())
