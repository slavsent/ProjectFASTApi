import redis

# для локального использования
#client = redis.Redis(host='127.0.0.1')
# для тестов docker
#client = redis.Redis(host='restoran_redis_pytest')
#для приложения в docker
client = redis.Redis(host='restoran_redis')

