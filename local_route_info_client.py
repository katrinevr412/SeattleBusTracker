import json
import os
from kcm_base_client import KCMBaseClient


class LocalRouteInfoClient(KCMBaseClient):

    def __init__(self):
        pass

    def get_route_info(self, route_ids, cache=True):
        in_out_bound_route_ids = self._plug_in_in_out_bound(route_ids)
        result = {}
        for route_id_ in in_out_bound_route_ids:
            with open(os.path.join('.', 'data', 'routes', str(route_id_) + '.txt'), 'r') as cache_file:
                response_data = json.load(fp=cache_file)
            result[route_id_] = response_data
        return self._process_route_response(result)
