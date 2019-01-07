from mongoengine import *


class ClipperItem(Document):

    date = DateTimeField()
    raw_note = StringField(required=True, unique=True)
    edited = BooleanField(default=False)
    edited_note = StringField()
    # hash = StringField(unique=True)
    visible = BooleanField(default=True)
    meta = {
        'indexes': [
            '#raw_note'  # hashed index
        ]
    }