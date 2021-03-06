"""
Link document.
"""
from mongoengine import (
  Document,
)
from mongoengine.fields import (
  StringField,
)
from utils import utils


class Link(Document):
    """
    Link representation.
    """

    meta = {'collection': 'links'}

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

    source = StringField()
    """
    :type: *str*
    :required: True
    :default: None
    """

    target = StringField()
    """
    :type: *str*
    :required: True
    :default: None
    """

    id = StringField(default="", primary_key=True)
