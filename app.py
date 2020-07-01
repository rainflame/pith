"""
Peruse following for more efficient updates:
- https://stackoverflow.com/questions/4372797/how-do-i-update-a-mongo-document-after-inserting-it
- https://stackoverflow.com/questions/33189258/append-item-to-mongodb-document-array-in-pymongo-without-re-insertion

If things go wonky, try:
sudo rm /var/lib/mongodb/mongod.lock
sudo service mongodb start
"""
import socketio
from uuid import UUID

from constants import (
    sio,
)
from discussion_constants import discussion_manager
from user_constants import user_manager
from utils.utils import UUIDEncoder


app = socketio.ASGIApp(sio)


@sio.on('get_posts')
async def get_posts(sid, json):
    discussion_id = json["discussion_id"]
    posts_data = discussion_manager.get_posts(discussion_id)
    return dumps(posts_data, cls=UUIDEncoder)


@sio.on('create_user')
async def create_user(sid, json):
    ip = json["user_id"]
    user_data = user_manager.create(ip)
    return dumps(user_data, cls=UUIDEncoder)


@sio.on('get_block')
async def get_block(sid, json):
    discussion_id = json["discussion_id"]
    block_id = json["block_id"]
    block_data = discussion_manager.get_block(discussion_id, block_id)
    return dumps(block_data, cls=UUIDEncoder)


@sio.on('save_post')
async def save_post(sid, json):
    user_id = json["user_id"]
    discussion_id = json["discussion_id"]
    post_id = json["post_id"]
    post_data = user_manager.save_post(user_id, discussion_id, post_id)
    serialized = dumps(post_data, cls=UUIDEncoder)
    await sio.emit("saved_post", serialized, to=sid) 
    return serialized


@sio.on('unsave_post')
async def unsave_post(sid, json):
    user_id = json["user_id"]
    discussion_id = json["discussion_id"]
    post_id = json["post_id"]
    post_data = user_manager.unsave_post(user_id, discussion_id, post_id)
    serialized = dumps(post_data, cls=UUIDEncoder)
    await sio.emit("unsaved_post", serialized, to=sid) 
    return serialized


@sio.on('save_block')
async def save_block(sid, json):
    user_id = json["user_id"]
    discussion_id = json["discussion_id"]
    block_id = json["block_id"]
    block_data = user_manager.save_block(user_id, discussion_id, block_id)
    serialized = dumps(block_data, cls=UUIDEncoder)
    await sio.emit("saved_block", serialized, to=sid) 
    return serialized


@sio.on('unsave_block')
async def unsave_block(sid, json):
    user_id = json["user_id"]
    discussion_id = json["discussion_id"]
    block_id = json["block_id"]
    block_data = user_manager.unsave_block(user_id, discussion_id, block_id)
    serialized = dumps(block_data, cls=UUIDEncoder)
    await sio.emit("unsaved_block", serialized, to=sid)
    return serialized


@sio.on('get_saved_posts')
async def get_saved_posts(sid, json):
    user_id = json["user_id"]
    discussion_id = json["discussion_id"]
    posts_data = user_manager.get_user_saved_posts(user_id, discussion_id)
    return dumps(posts_data, cls=UUIDEncoder)


@sio.on('get_saved_blocks')
async def get_saved_blocks(sid, json):
    user_id = json["user_id"]
    discussion_id = json["discussion_id"]
    blocks_data = user_manager.get_user_saved_blocks(user_id, discussion_id)
    return dumps(blocks_data, cls=UUIDEncoder)


@sio.on('post_add_tag')
async def post_add_tag(sid, json): 
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    post_id = json["post_id"]
    tag = json["tag"] 
    discussion_manager.post_add_tag(discussion_id, user_id, post_id, tag)
    serialized = dumps({"post_id": post_id, "user_id": user_id, "tag": tag}, \
        cls=UUIDEncoder, broadcast=True)
    await sio.emit("tagged_post", serialized)
    return serialized


@sio.on('post_remove_tag')
async def post_remove_tag(sio, json): 
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    post_id = json["post_id"]
    tag = json["tag"]
    discussion_manager.post_remove_tag(discussion_id, user_id, post_id, tag)
    serialized = dumps({"post_id": post_id, "tag": tag}, \
        cls=UUIDEncoder, broadcast=True)
    await sio.emit("untagged_post", serialized)
    return serialized


@sio.on('block_add_tag')
async def block_add_tag(sio, json): 
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    block_id = json["block_id"]
    tag = json["tag"] 
    discussion_manager.block_add_tag(discussion_id, user_id, block_id, tag)
    serialized = dumps({"block_id": block_id, "user_id": user_id, "tag": tag}, \
        cls=UUIDEncoder)
    await sio.emit("tagged_block", serialized)
    return serialized


@sio.on('block_remove_tag')
async def block_remove_tag(sio, json): 
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    block_id = json["block_id"]
    tag = json["tag"]
    discussion_manager.block_remove_tag(discussion_id, user_id, block_id, tag)
    serialized = dumps({"block_id": block_id, "tag": tag}, \
        cls=UUIDEncoder)
    await sio.emit("untagged_block", serialized)
    return serialized


@sio.on('create_discussion')
async def create_discussion(sio, json):
    discussion_data = discussion_manager.create()
    serialized = dumps(discussion_data, cls=UUIDEncoder)
    await sio.emit("created_discussion", serialized)
    return serialized


@sio.on('join_discussion')
async def join_discussion(sio, json):
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    discussion_data = discussion_manager.join(discussion_id, user_id)
    serialized = dumps(discussion_data, cls=UUIDEncoder)
    await sio.emit("joined_discussion", serialized)
    return serialized


@sio.on('leave_discussion')
async def leave_discussion(sio, json):
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    discussion_data = discussion_manager.leave(discussion_id, user_id)
    serialized = dumps(discussion_data, cls=UUIDEncoder)
    await sio.emit("left_discussion", serialized)
    return serialized


@sio.on('create_post')
async def create_post(sio, json):
    discussion_id = json["discussion_id"]
    user_id = json["user_id"]
    blocks = json["blocks"]
    post_data = discussion_manager.create_post(discussion_id, user_id, blocks)
    serialized = dumps(post_data, cls=UUIDEncoder)
    await sio.emit("created_post", serialized)
    return serialized


@sio.on('search_discussion')
async def search_discussion(sio, json):
    discussion_id = json["discussion_id"]
    query = json["query"]
    result = discussion_manager.discussion_scope_search(discussion_id, query)
    serialized = dumps(result, cls=UUIDEncoder, to=sid)
    return serialized


@sio.on('search_user_saved')
async def search_user_saved(sio, json):
    user_id = json["user_id"]
    query = json["query"]
    result = user_manager.user_saved_scope_search(user_id, query)
    serialized = dumps(result, cls=UUIDEncoder, to=sid)
    return serialized
