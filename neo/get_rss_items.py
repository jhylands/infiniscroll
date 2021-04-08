# The purpose of this module is to provide an interface that
# allows for access to the items

from py2neo import Graph
from py2neo.ogm import Model, Property, Label, RelatedTo, RelatedFrom
graph = Graph(password="test")



def get_items(feed):
    return get_user(1).subscribed_to

def get_user(user_id):
    return User.match(graph).where(id=user_id).first()


class Feed(Model):
    name = Property("name")
    url = Property("url")

    subscribers = RelatedFrom("User", "SUBSCRIBED")
    items = RelatedFrom("FeedItem")

class User(Model):
    id = Property("id")
    name = Property("name")
    email = Property("email")

    subscribed_to = RelatedTo(Feed, "SUBSCRIBED")

class FeedItem(Model):
    title = Property()
    link = Property()
    img = Property()

    date = Property()

    source = RelatedTo(Feed, "SOURCE")
    
