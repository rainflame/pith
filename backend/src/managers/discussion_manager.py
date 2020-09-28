import datetime
import logging
from typing import (
  Any,
  Dict,
  List,
  Optional,
  Tuple,
)

import constants
import error
from search.search import search
from utils import utils

from models.discussion import (
  Unit,
  User,
  Discussion,
)


class DiscussionManager:

    def __init__(self, gm):
        self.gm = gm
        self.redis_queue = self.gm.redis_queue

    # pointer
    def _get(self, discussion_id):
        return Discussion.objects(id=discussion_id)

    def create_user(self, discussion_id, nickname):
        discussion = self._get(discussion_id)
        unit_id = discussion.get().document
        cursor = Cursor(unit_id, -1) 
        user = User(name=nickname, cursor=cursor) 
        discussion.update(push__users=user)
        response = {"user_id": user.id}
        return response

    def join(self, discussion_id, user_id):
        discussion = self._get(discussion_id)
        discussion.filter(users__id=user_id).update(users__S__active=True) 
        nickname = discussion.get().users.filter(id=user_id).name
        response = {"nickname": nickname}
        return nickname

    def leave(self, discussion_id, user_id):
        discussion = self._get(discussion_id)
        discussion.filter(users__id=user_id).update(users__S__active=False) 
        nickname = discussion.get().users.filter(id=user_id).name
        response = {"nickname": nickname}
        return nickname

    def load(self, discussion_id, user_id):
        discussion = self._get(discussion_id)

    def get_unit_page(self, discussion_id, unit_id):
        discussion = self._get(discussion_id)

    def get_ancestors(self, discussion_id, unit_id):
        discussion = self._get(discussion_id)

    def get_unit_content(self, discussion_id, unit_id):
        discussion = self._get(discussion_id)
  
    def get_unit_context(self, discussion_id, unit_id):
        discussion = self._get(discussion_id)

    def post(self, discussion_id, user_id, piths):
        discussion = self._get(discussion_id)

    def search(self, discussion_id, query):
        discussion = self._get(discussion_id)
      
    def send_to_doc(self, discussion_id, user_id, unit_id):
        discussion = self._get(discussion_id)

    def move_cursor(self, discussion_id, user_id, position):
        discussion = self._get(discussion_id)

    def hide_unit(self, discussion_id, unit_id):
        """ change state, do not return """
        discussion = self._get(discussion_id)

    def unhide_unit(self, discussion_id, unit_id):
        """ change state, do not return """
        discussion = self._get(discussion_id)

    def added_unit(self, discussion_id, user_id, pith):
        discussion = self._get(discussion_id)

    def select_unit(self, discussion_id, user_id, unit_id):
        discussion = self._get(discussion_id)

    def move_units(self, discussion_id, user_id, units, parent):
        discussion = self._get(discussion_id)

    def merge_units(self, discussion_id, user_id, units, parent):
        discussion = self._get(discussion_id)

    def request_to_edit(self, discussion_id, user_id, unit_id):
        discussion = self._get(discussion_id)

    def edit_unit(self, discussion_id, unit_id, pith):
        discussion = self._get(discussion_id)
