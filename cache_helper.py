import redis
import ast


r = redis.Redis(host='localhost', port=6379, db=0)


def set(key, value):
    try:
        r.set(key, str(value))
        return True

    except redis.exceptions.ConnectionError:
        return None


def get(key):
    try:
        ret = r.get(key)
        if ret:
            return ast.literal_eval(ret.decode("utf-8"))
        return None

    except redis.exceptions.ConnectionError:
        return None

    except ValueError:
        return None
