from error import Errors
from pymongo import ASCENDING

from utils.utils import (
  make_error,
)
from models.unit import Unit

from managers.checker import Checker


class DiscussionManager:

    def __init__(self, gm):
        self.gm = gm

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_user_id
    def join_disc(self, board_id, discussion_id, user_id):
      self.gm.users.update_one(
        {"short_id" : user_id, "board_id": board_id},
        {"$set": {"discussion_id": discussion_id}}
      )
      return {"user": self.gm._get_user(board_id, user_id)}

    @Checker._check_board_id
    @Checker._check_discussion_id
    def load_disc(self, board_id, discussion_id):
      discussion = self.gm.discussions.find_one({"short_id": discussion_id, "board_id": board_id})
      (chat, end_index) = self.gm._chat_page(board_id, discussion_id)
      return {
        "end_index": end_index, # actually start index
        "chat": chat,
        "pinned": [self.gm._get_chat_unit(board_id, u) for u in discussion["pinned"]],
        "focused": [self.gm._get_basic_unit(board_id, u) for u in discussion["focused"]],
        "participants": self.gm._get_participants(board_id, discussion_id)
      }

    @Checker._check_board_id
    @Checker._check_discussion_id
    def load_chat_page(self, board_id, discussion_id, end_index):
        (chat, end_index) = self.gm._chat_page(board_id, discussion_id, end_index)
        return {
          "end_index": end_index,
          "chat_page": chat
        }

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_user_id
    def leave_disc(self, board_id, discussion_id, user_id):
      self.gm.users.update_one(
        {"short_id" : user_id, "board_id": board_id},
        {"$set": {"discussion_id": None}}
      )
      return {"user": self.gm._get_user(board_id, user_id)}

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_user_id
    def post(self, board_id, discussion_id, user_id, text, flairs):
      pith, transclusions = self.gm._get_pith(board_id, text)
      user = self.gm.users.find_one({"board_id": board_id, "short_id": user_id})

      unit = Unit(board_id=board_id, pith=pith, chat=True, 
        author=user_id, author_name=user["nickname"], flairs=flairs)
      unit.id = "{}:{}".format(unit.board_id, unit.short_id)

      self.gm.units.insert_one(unit.to_mongo())
      unit_id = unit.short_id
      self.gm._insert_transclusions(board_id, unit_id, transclusions)
      self.gm.discussions.update_one(
        {"short_id" : discussion_id, "board_id": board_id},
        {"$push": {"chat": unit_id}}
      )
      return {"unit": self.gm._get_chat_unit(board_id, unit_id)}

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_unit_id
    def add_pinned(self, board_id, discussion_id, unit_id, user_id):
      unit = self.gm.units.find_one({"short_id": unit_id, "board_id": board_id})
      if unit["chat"] is False:
        return make_error(Errors.NOT_CHAT, 
          error_meta={"unit_id": unit_id}
        )

      discussion = self.gm.discussions.find_one({"short_id": discussion_id, "board_id": board_id})
      if unit["short_id"] not in discussion["pinned"]:
        self.gm.discussions.update_one(
            {"short_id" : discussion_id, "board_id": board_id},
            {"$addToSet": {"pinned": unit_id}}
        )

        message = "pinned \"{}\"".format(unit["pith"])
        notice_unit = self.gm.create_notice_unit(board_id, discussion_id, message, user_id)

        return {
          "unit": self.gm._get_chat_unit(board_id, unit_id),
          "notice_unit": self.gm._get_chat_unit(board_id, notice_unit.short_id)
        }
      else:
        return {}

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_unit_id
    def remove_pinned(self, board_id, discussion_id, unit_id, user_id):
      self.gm.discussions.update_one(
        {"short_id" : discussion_id, "board_id": board_id},
        {"$pull": {"pinned": unit_id}}
      )

      unit = self.gm.units.find_one({"short_id": unit_id, "board_id": board_id})
      message = "unpinned \"{}\"".format(unit["pith"])
      notice_unit = self.gm.create_notice_unit(board_id, discussion_id, message, user_id)

      return {
        "unit_id": unit_id,
        "notice_unit": self.gm._get_chat_unit(board_id, notice_unit.short_id)
      }

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_unit_id
    def add_focused(self, board_id, discussion_id, unit_id):
      unit = self.gm.units.find_one({"short_id": unit_id, "board_id": board_id})
      if unit["chat"] is True:
        return make_error(Errors.NOT_BOARD, 
          error_meta={"unit_id": unit_id}
        )

      discussion = self.gm.discussions.find_one({"short_id": discussion_id, "board_id": board_id})
      if unit["short_id"] not in discussion["focused"]:
        self.gm.discussions.update_one(
            {"short_id" : discussion_id, "board_id": board_id},
            {"$addToSet": {"focused": unit_id}}
        )
        return {"unit": self.gm._get_basic_unit(board_id, unit_id)}
      else:
        return {}

    @Checker._check_board_id
    @Checker._check_discussion_id
    @Checker._check_unit_id
    def remove_focused(self, board_id, discussion_id, unit_id):
      self.gm.discussions.update_one(
        {"short_id" : discussion_id, "board_id": board_id},
        {"$pull": {"focused": unit_id}}
      )
      return {"unit_id": unit_id}

    @Checker._check_board_id
    @Checker._check_discussion_id
    def search(self, board_id, discussion_id, query):
      discussion = self.gm.discussions.find_one(
        {"board_id": board_id, "short_id": discussion_id}
      )
      chat_ids = discussion["chat"]
      # query is OR-based      
      results = [u["short_id"] for u in self.gm.units.find({
        "board_id": board_id,
        "short_id": {"$in": chat_ids},
        "$text": {"$search": query}
      }).sort([("created", ASCENDING)])]
      return {"results": [self.gm._get_chat_unit(board_id, r) for r in results]}
