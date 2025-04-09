from neomodel import StructuredNode, StringProperty, RelationshipTo, db
import uuid
from datetime import datetime


class User(StructuredNode):
    uid = StringProperty(unique_index=True, default=lambda: str(uuid.uuid4()))
    username = StringProperty(required=True)

class Book(StructuredNode):
    uid = StringProperty(unique_index=True, default=lambda: str(uuid.uuid4()))
    title = StringProperty(required=True)
    author = StringProperty(required=True)

class Quote(StructuredNode):
    uid = StringProperty(unique_index=True, default=lambda: str(uuid.uuid4()))
    text = StringProperty(required=True)
    preview = StringProperty()  # First 5 words
    timestamp = StringProperty(default=lambda: datetime.now().isoformat())
    posted_by = RelationshipTo('User', 'POSTED')
    references = RelationshipTo('Book', 'REFERENCES')

    def save(self, *args, **kwargs):
        # Set preview to first 5 words
        words = self.text.split()
        self.preview = ' '.join(words[:5])
        return super().save(*args, **kwargs)
        