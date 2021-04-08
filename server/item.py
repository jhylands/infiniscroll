# The idea behind this class is that it represents an item which will be leaded into the feed

class Item:
    def __init__(self, title):
        # the item at least needs a title, right?
        self.title = title
