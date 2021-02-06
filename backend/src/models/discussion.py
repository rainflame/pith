"""
Discussion document.
"""
from mongoengine import (
  Document,
  PULL,
)
from mongoengine.fields import (
  BooleanField,
  DateTimeField,
  DictField,
  EmbeddedDocumentField,
  EmbeddedDocumentListField,
  IntField,
  ListField,
  ReferenceField,
  StringField,
)
from datetime import datetime
import utils


class Discussion(Document):
    """
    Discussion representation.
    """

    meta = {'collection': 'discussions'}

    id = StringField(default=utils.gen_key(), primary_key=True)
    """
    :type: *str*
    :required: False
    :default: Automatically generated.
    """

    created = DateTimeField(default=utils.get_time())
    """
    :type: *datetime*
    :required: False
    :default: Automatically generated.
    """

    board_id = StringField()
    """
    :type: *str*
    :required: True
    :default: None
    """

    chat = ListField(StringField(), default=[]) # unit ids
    """
    :type: *List[str]*
    :required: False
    :default: []
    """

    pinned = ListField(StringField(), default=[]) # unit ids
    """
    :type: *List[str]*
    :required: False
    :default: []
    """

    focused = ListField(StringField(), default=[]) # unit ids
    """
    :type: *List[str]*
    :required: False
    :default: []
    """

    participants = ListField(StringField(), default=[]) 
    """
    :type: *List[str]*
    :required: False
    :default: []
    """
