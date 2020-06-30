"""
API relating to the user.
"""
from models.user import User


class UserManager:

    def __init__(self, db):
        self.users = db["users"]

    """
    Of users.
    """

    def get_all(self):
        user_cursor = self.users.find()
        user_list = []
        for u in user_cursor:
            user_list.append(u)
        return user_list

    def get(self, user_id):
        user_data = self.users.find_one({ "_id" : user_id })
        return user_data

    def _insert(self, user_obj):
        user_data = user_obj.__dict__
        self.users.insert_one(user_data)

    def _is_user(self, user_id):
        user_data = self.get(user_id)
        return not (user_data is None)

    def create(self, ip):
        user_data = self.get(ip)
        if not self.is_user(ip):
            user_obj = User(ip)
            self._insert_user(user_obj)
            user_data = user_obj.__dict__
        return user_data

    """
    Within a user.
    First arg is always `user_id`.
    TODO maybe use a wrapper that takes in user_id and gives user_data.
    """

    def _is_discussion_user(self, user_id, discussion_id):
        user_data = self.get(user_id)
        return discussion_id in user_data["discussions"]

    def _is_active_discussion(self, user_id, discussion_id):
        """
        A discussion is not active if it is
        1) not made,
        2) not active.
        """
        if discussion_id not in user_data["discussions"]: return True
        return user_data["discussions"][discussion_id]["active"]

    def join_discussion(self, user_id, discussion_id):
        """
        Discussion should check we are not in, or active.
        """
        assert(not self._is_active_discussion(user_id, discussion_id))
        user_data = self.get(user_id)
        if self._is_discussion_user(user_id, discussion_id): # rejoin
            user_data["discussions"][discussion_id]["active"] = True
        else:
            user_data["discussions"][discussion_id] = {
                "active": True,
                "library": {
                    "posts": [],
                    "blocks": [],
                } 
            }

    def leave_discussion(self, user_id, discussion_id):
        """
        Discussion should check we are in, or active.
        """
        assert(self._is_active_discussion(user_id, discussion_id))
        user_data = self.get(user_id)
        user_data["discussions"][discussion_id]["active"] = False

    def insert_post_user_history(self, user_id, discussion_id, post_id):
        self.users.update_one({"_id" : user_id}, {"$push": \
            {"discussions.{}.history".format(discussion_id) : post_id}})

    def _is_saved_post(self, user_id, discussion_id, post_id):
        user_data = self.get(user_id)
        return post_id in user_data["discussions"][discussion_id]["library"]["posts"]

    def save_post(self, user_id, discussion_id, post_id):
        if not self._is_saved_post(user_id, discussion_id, post_id):
            self.users.update_one({"_id" : user_id}, {"$push" : \
                {"discussions.{}.library.posts".format(discussion_id) : post_id}})

    def unsave_post(self, user_id, discussion_id, post_id):
        if self._is_saved_post(user_id, discussion_id, post_id):
            self.users.update_one({"_id" : user_id}, {"$pull" : \
                {"discussions.{}.library.posts".format(discussion_id) : post_id}})

    def get_user_saved_posts(self, user_id, discussion_id):
        user_data = self.get(user_id)
        return user_data["discussions"][discussion_id]["library"]["posts"]

    def is_saved_block(self, user_id, discussion_id, block_id):
        user_data = self.get(user_id)
        return block_id in user_data["discussions"][discussion_id]["library"]["blocks"]

    def save_block(self, user_id, discussion_id, block_id):
        if not self._is_saved_block(user_id, discussion_id, block_id):
            self.users.update_one({"_id" : user_id}, {"$push" : \
                {"discussions.{}.library.blocks".format(discussion_id) : block_id}})

    def unsave_block(self, user_id, discussion_id, block_id):
        if self._is_saved_block(user_id, discussion_id, block_id):
            self.users.update_one({"_id" : user_id}, {"$pull" : \
                {"discussions.{}.library.blocks".format(discussion_id) : block_id}})

    def get_user_saved_blocks(self, user_id, discussion_id):
        user_data = self.get(user_id)
        return user_data["discussions"][discussion_id]["library"]["blocks"]

    def user_saved_scope_search(self, user_id, discussion_id, query):
        post_ids = self.get_user_saved_posts(user_id, discussion_id)
        block_ids = self.get_user_saved_blocks(user_id, discussion_id)
        posts_obj = {
            p: Post(**discussion_manager.get_post(discussion_id, p)) \
            for p in post_ids
        }
        blocks_obj = {
            b: Block(**discussion_manager.get_block(discussion_id, b)) \
            for b in block_ids
        }
        return basic_search(query, block_ids, post_ids)