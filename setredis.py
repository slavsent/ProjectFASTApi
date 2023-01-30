import redis
import os


local = os.environ.get("Local")

if local:
    # для локального использования
    client = redis.Redis(host='127.0.0.1')
    # для тестов docker
    #client = redis.Redis(host='restoran_redis_pytest')
    #для приложения в docker
    #client = redis.Redis(host='restoran_redis')
else:
    client = redis.Redis(host='restoran_redis')
