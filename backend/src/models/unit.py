"""
Unit document.
"""
from mongoengine import (
  Document,
  EmbeddedDocument,
)
from mongoengine.fields import (
  BooleanField,
  ListField,
  StringField,
  IntField,
  EmbeddedDocumentField,
)

from utils import utils
import constants


class Position(EmbeddedDocument):
    x = IntField(min_value=0, max_value=constants.FULL_SIZE)

    y = IntField(min_value=0, max_value=constants.FULL_SIZE)


class Unit(Document):
    """
    Unit representation.
    Text-searchable over `pith`.
    """

    meta = {'collection': 'units'}

    short_id = StringField(default=lambda: utils.gen_key())
    """
    :type: *str*
    :required: False
    :default: Automatically generated.
    """

    created = StringField(default=lambda: utils.get_time())
    """
    :type: *str*
    :required: False
    :default: Automatically generated.
    """

    board_id = StringField()
    """
    :type: *str*
    :required: True
    :default: None
    """

    pith = StringField(required=True)
    """
    :type: *str*
    :required: True
    :default: None
    """

    position = EmbeddedDocumentField(Position)

    chat = BooleanField(default=False) # versus in document
    """
    :type: *bool*
    :required: False
    :default: False
    """

    author = StringField()
    """
    :type: *str*
    :required: False
    :default: None
    """

    author_name = StringField()
    """
    :type: *str*
    :required: False
    :default: None
    """

    flairs = ListField(StringField(), default=[])
    """
    :type:
    :required: False
    :default: []
    """

    hidden = BooleanField(default=False)
    """
    :type: *bool*
    :required: False
    :default: False
    """
    
    notice = BooleanField(default=False)
    """
    :type: *bool*
    :required: False
    :default: False
    """

    id = StringField(default="", primary_key=True)
