import mongoengine as me
from app.extensions import db

def min_items(val):
    if len(val) < 1:
        raise me.ValidationError("List must contain at least 1 item.")

class User(db.Document):
    meta = {'collection': 'users'}
    name = me.StringField(required=True, max_length=100)
    domains = me.ListField(me.StringField(), validation = min_items)