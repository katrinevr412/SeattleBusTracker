from route_info_cache import RouteInfoCache
from rubbishy_kcm_vehicle_tracker.constants import Constants
from rubbishy_kcm_vehicle_tracker.client.kcm_api_client import KingCountyMetroRealTimeAPIClient
from multiprocessing.pool import Pool
from functools import partial


def write_to_cache(route, cache_loader):
    route_dict = cache_loader.api_client.get_raw_route_info_response([route])
    for route_ in route_dict:
        cache_loader.cache_client.write(route_, route_dict[route_])


class CacheLoader:

    def __init__(self):
        self.cache_client = RouteInfoCache()
        self.api_client = KingCountyMetroRealTimeAPIClient()

    def load(self, parallel=True):
        self.cache_client.clear()
        if parallel:
           result = Pool(len(Constants.ALL_LINES)).imap_unordered(
               partial(write_to_cache, cache_loader=self),
               Constants.ALL_LINES
           )
           for _ in result:
               pass
        else:
            for route in Constants.ALL_LINES:
                write_to_cache(route, self)
