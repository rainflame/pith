import os
import re

from arq.connections import RedisSettings

from dotenv import load_dotenv


load_dotenv()


# the port to run the socketio server 
PORT = os.getenv("PORT", 8080)

# connect to the redis server instance. When running locally, use 127.0.0.1, or
# use the container name if using docker within a docker network
SOCKET_REDIS = "redis://{}:{}/0".format(os.getenv("REDIS_IP", "127.0.0.1"), os.getenv("REDIS_PORT", 6379))

# the job queue's redis configuration. Could use a different redis server
# instance than the socket message queue, but for now we can keep them the same.
ARQ_REDIS = RedisSettings(host=os.getenv("REDIS_IP", "127.0.0.1"), port=int(os.getenv("REDIS_PORT", 6379)))

# the maximum number to times we should try to rerun a task in the queue if it fails
MAX_QUEUED_JOB_RETRIES = 5
# the maximum number of jobs we should try to run at once from the queue
MAX_JOBS = 10

# using ISO so this can be easily parsed in js with Date()
DATE_TIME_FMT = "%Y-%m-%dT%H:%M:%S.000Z"
MONGODB_CONN = os.getenv("MONGODB_CONN", "mongodb://localhost:27017")
MONGODB_NAME = os.getenv("MONGODB_NAME", "pith")

# file we log to
LOG_FILENAME = "app_log"

# compiled searcher for link pattern
#LINK_PATTERN = re.compile(r"<cite>([^<]*)<\/cite>")
#LINK_WRAPPER = "<cite>{}</cite>"
#DEAD_LINK = "<cite></cite>"
LINK_REGEX = r"\[\[\s*(.*?)\s*\]\]"
LINK_PATTERN = re.compile(LINK_REGEX)
LINK_WRAPPER = "[[{}]]"
LINK_NULL = "[.]"

CHAT_PAGE_SIZE = 25
BOARD_UPDATE_DURATION = 10 # seconds

# 2D board
FULL_SIZE = 1500
