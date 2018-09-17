import os
import json


class RouteInfoCache:

    def __init__(self):
        self.caching_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'routes'))
        if not os.path.exists(self.caching_dir):
            os.makedirs(self.caching_dir)

    def write(self, route_id, json_obj):
        with open(self.__get_cache_file_path(route_id), 'w') as _cache:
            json.dump(obj=json_obj, fp=_cache)

    def read(self, route_id):
        with open(self.__get_cache_file_path(route_id), 'r') as _cache:
            return json.load(fp=_cache)

    def delete(self, route_id):
        os.remove(self.__get_cache_file_path(route_id))

    def clear(self):
        for filename in os.listdir(self.caching_dir):
            os.remove(os.path.join(self.caching_dir, filename))

    def list_all_cached_routes(self):
        cached_routes = []
        for filename in os.listdir(self.caching_dir):
            cached_routes.append(os.path.splitext(filename)[0])
        return cached_routes

    def __get_cache_file_path(self, route_id):
        return os.path.join(self.caching_dir, str(route_id) + '.txt')
