from kcm_base_client import KCMBaseClient


class KCMLocalRouteInfoClient(KCMBaseClient):

    def __init__(self):
        KCMBaseClient.__init__(self)

    def get_route_info(self, route_ids, cache=True):
        in_out_bound_route_ids = self._plug_in_in_out_bound(route_ids)
        result = {}
        for route_id_ in in_out_bound_route_ids:
            result[route_id_] = self.cache_client.read(route_id_)
        return self._process_route_response(result)
