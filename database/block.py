"""
Block getters and setters 
"""

from constants import (
    blocks,        
)
from discussion import (
    get_discussion,        
)
from user import (
    get_user,        
)


class BlockDatabase:

    def get_blocks(self):
        block_cursor = blocks.find()
        block_list = []
        for u in block_cursor:
            block_list.append(u)
        return block_list

    def get_discussion_blocks(self, discussion_id):
        discussion_data = get_discussion(discussion_id)
        history = discussion_data["history_blocks"]
        return history

    def get_user_saved_blocks(self, user_id):
        user_data = get_user(user_id)
        saved = user_data["library"]["blocks"]
        return saved

    def get_block(self, block_id):
        block_data = blocks.find_one({ "_id" : block_id })
        return block_data

    def insert_block(self, block_obj):
        block_data = block_obj.__dict__
        blocks.insert_one(block_data)

    def save_block(self, block_id, user_id):
        users.update_one({"_id" : user_id}, {"$push" : {"library.blocks" : block_id}})

    def unsave_block(self, block_id, user_id):
        users.update_one({"_id" : user_id}, {"$pull" : {"library.blocks" : block_id}})

    def block_add_tag(self, block_id, tag):
        blocks.update_one({"_id" : block_id}, {"$push": {"tags" : tag}})

    def block_remove_tag(self, block_id, tag):
        blocks.update_one({"_id" : block_id}, {"$pull": {"tags" : tag}})
