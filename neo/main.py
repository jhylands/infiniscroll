# The purpose of this module is to provide an interface that
# allows for access to the items

from typing import List
from py2neo import Graph
from py2neo.ogm import Model, Property, RelatedTo, RelatedFrom
import os

graph = Graph(host="bolt.timep.co.uk", password=os.environ["neocode"])


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
        results = graph.run(
            """
match (a:FeedItem {{attribute:\"{}\"}})-[:PROPERTY*..4]->(n:FeedItem)
where ID(n)={} return a limit 1;
""".format(
                key, self.__primaryvalue__
            )
        )
        return FeedItem.wrap(results.evaluate())

    def get_properties(self, properties: List[str]):

        match_clause = (
            "match (a:FeedItem )-[:PROPERTY*..4]->(self)-[:SOURCE]->(feed:Feed)"
        )
        # WHERE
        id_clause = "id(feed)=$feed_id and id(self)=$self_id"
        property_table = [("$a_{}".format(i), a) for i, a in enumerate(properties)]
        properties_clause = " or ".join(
            ['a.attribute="{}"'.format(title) for title, attribute in property_table]
        )
        return_clause = "a"
        query = f"{match_clause} where {id_clause} and  ({properties_clause}) return {return_clause}"
        print(query)
        key_dict = {
            **dict(property_table),
            **{"self_id": self.__primarykey__, "feed_id": "2"},
        }
        data = graph.run(query, **key_dict).data()
        return dict([(v["a"]["attribute"], v["a"]["value"]) for v in data])
