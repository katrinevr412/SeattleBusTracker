from kcm_api_client import KingCountyMetroRealTimeAPIClient
from kcm_local_route_info_client import KCMLocalRouteInfoClient


class KCMRouteInfoProxy:

    def __init__(self):
        self.local_client = KCMLocalRouteInfoClient()
        self.remote_client = KingCountyMetroRealTimeAPIClient()

    def get_route_info(self, route_ids, cache=True, refresh_cache=False):
        if not cache:
            # if cache not specified, fallback to remote client.
            return self.remote_client.get_route_info(route_ids, cache=False)
        if refresh_cache:
            # if cache is forced to be refreshed, fetch it from remote client.
            return self.remote_client.get_route_info(route_ids)
        try:
            # always favour local client in terms of efficiency
            return self.local_client.get_route_info(route_ids)
        except:
            return self.remote_client.get_route_info(route_ids)
