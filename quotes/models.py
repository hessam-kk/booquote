from neomodel import (
    StructuredNode, StringProperty, RelationshipTo,RelationshipFrom, StructuredRel,
    DateProperty, IntegerProperty, FloatProperty, db
)
import uuid
from datetime import datetime

# Custom relationship for READ with properties
class ReadRel(StructuredRel):
    date_of_finishing = DateProperty(required=True)  # Date when the user finished the book
    score = IntegerProperty(required=True, choices=[(i, i) for i in range(1, 6)])  # Score from 1 to 5
    duration_of_reading = FloatProperty(required=True)  # Duration in days (e.g., 5.5 days)
    notes = StringProperty(default="")  # Optional notes about the book
    
    
class User(StructuredNode):
    uid = StringProperty(unique_index=True, default=lambda: str(uuid.uuid4()))
    username = StringProperty(required=True)
    # Relationships
    posted = RelationshipTo('Quote', 'POSTED BY')
    read = RelationshipTo('Book', 'READ', model=ReadRel)  # New READ relationship

class Book(StructuredNode):
    uid = StringProperty(unique_index=True, default=lambda: str(uuid.uuid4()))
    title = StringProperty(required=True)
    author = StringProperty(required=True)
    # Relationships
    quotes = RelationshipFrom('Quote', 'REFERENCE')
    read_by = RelationshipFrom('User', 'READ', model=ReadRel)  # Incoming READ relationship
    
    
class Quote(StructuredNode):
    uid = StringProperty(unique_index=True, default=lambda: str(uuid.uuid4()))
    text = StringProperty(required=True)
    preview = StringProperty()  # First 5 words
    timestamp = StringProperty(default=lambda: datetime.now().isoformat())
    posted_by = RelationshipTo('User', 'POSTED BY')
    references = RelationshipTo('Book', 'REFERENCE')

    def save(self, *args, **kwargs):
        # Set preview to first 5 words
        words = self.text.split()
        self.preview = ' '.join(words[:5])
        return super().save(*args, **kwargs)
        