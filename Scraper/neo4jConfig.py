from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
                      UniqueIdProperty, RelationshipTo, RelationshipFrom, DateTimeProperty, DateProperty)

class Post(StructuredNode):
    video_url = StringProperty(unique_index=True)
    description = StringProperty()
    nrComments = IntegerProperty()
    nrLikes = IntegerProperty()
    nrForwarded = IntegerProperty()
    date=DateProperty()
    created = DateTimeProperty(default_now=True)
    user = RelationshipFrom('User','POSTED')
    hashtags = RelationshipTo("Hashtag","INCLUDES")
    music = RelationshipTo("Music", "INCLUDES")
    mentionedUser =RelationshipTo("User","MENTIONS")


class User(StructuredNode):
    username = StringProperty()
    userScreenname = StringProperty(unique_index=True)
    posts = RelationshipTo("Post","POSTED")
    mentions = RelationshipFrom("Post", "MENTIONS")
    created = DateTimeProperty(default_now=True)

class Hashtag(StructuredNode):
    name = StringProperty(unique_index=True)
    posts = RelationshipFrom("Post","INCLUDES")
    created = DateTimeProperty(default_now=True)

class Music(StructuredNode):
    title =StringProperty(unique_index=True)
    url   =StringProperty()
    posts = RelationshipFrom("Post", "INCLUDES")
    created = DateTimeProperty(default_now=True)

