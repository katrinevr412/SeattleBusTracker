import json
from route_info_cache import RouteInfoCache


class CacheChecker:

    def __init__(self):
        self.cache_client = RouteInfoCache()
        self.invalid = '{"version": "1.1", "result": {"stops": [], "lineTraces": {"patternTraces": [], "zoom": {}}}}'

    def check(self, delete=False):
        bad_routes = []
        for route in self.cache_client.list_all_cached_routes():
            content = self.cache_client.read(route)
            if len(json.dumps(content)) <= len(self.invalid) + 4:
                bad_routes.append(int(route))

        if len(bad_routes):
            print "Bad cache for routes detected: %s" % sorted(bad_routes)
        else:
            print "All route caches are good."

        if delete:
            for route in bad_routes:
                self.cache_client.delete(str(route))
