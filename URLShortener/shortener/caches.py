import json

from URLShortener.redis_app import redis_app as redis


class URLCache:
    """
    The cached data might be inconsistency.
    It's used for avoiding the queries for most of the conditions.
    """
    KEY_HASH_URL_MAP = 'HashURLMap'
    KEY_URL_HASH_MAP = 'URLHashMap'

    @classmethod
    def get_hash_url_map(cls):
        return cls._get_or_set_map(cls.KEY_HASH_URL_MAP)

    @classmethod
    def get_url_hash_map(cls):
        return cls._get_or_set_map(cls.KEY_URL_HASH_MAP)

    @classmethod
    def set_hash_url_map(cls, map_to_set):
        return cls._get_or_set_map(cls.KEY_HASH_URL_MAP, map_to_set)

    @classmethod
    def set_url_hash_map(cls, map_to_set):
        return cls._get_or_set_map(cls.KEY_URL_HASH_MAP, map_to_set)

    @classmethod
    def _get_or_set_map(cls, key, map_to_set=None):
        if map_to_set:
            redis.set(key, json.dumps(map_to_set))
            return map_to_set

        cached = redis.get(key)
        if cached is None:
            return {}
        return json.loads(redis.get(key))

    @classmethod
    def get_url(cls, hash):
        hash_url_map = cls.get_hash_url_map()
        return hash_url_map.get(hash, None)

    @classmethod
    def get_hash(cls, url):
        url_hash_map = cls.get_url_hash_map()
        return url_hash_map.get(url, None)

    @classmethod
    def set(cls, hash_url_pairs):
        hash_url_map = cls.get_hash_url_map()
        url_hash_map = cls.get_url_hash_map()

        for hash, url in hash_url_pairs:
            hash_url_map[hash] = url
            url_hash_map[url] = hash

        cls.set_hash_url_map(hash_url_map)
        cls.set_url_hash_map(url_hash_map)
