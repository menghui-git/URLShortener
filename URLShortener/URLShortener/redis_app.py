import os

from redis import Redis


redis_app = Redis(host=os.environ['REDIS_HOST'],
                  port=os.environ['REDIS_PORT'])
