from rubbishy_kcm_vehicle_tracker.components.stop import Stop
from rubbishy_kcm_vehicle_tracker.components.pattern import Pattern
from rubbishy_kcm_vehicle_tracker.components.route import Route
from rubbishy_kcm_vehicle_tracker.cache.route_info_cache import RouteInfoCache
from rubbishy_kcm_vehicle_tracker.utils.utils import Utils


class KCMBaseClient:

    def __init__(self):
        self.cache_client = RouteInfoCache()

    def _process_route_response(self, result):
        res = {}
        for route_id in result:
            response_data = result[route_id]
            stops = response_data['result']['stops']
            patterns = response_data['result']['lineTraces']['patternTraces']
            res[route_id] = Route(route_id,
                     [Stop.deserialize_from_json_obj(stop) for stop in stops],
                     [Pattern.deserialize_from_json_obj(pattern) for pattern in patterns])
        return res

    def _plug_in_in_out_bound(self, route_ids):
        result = []
        for route_id in route_ids:
            inbound_suffix, outbound_suffix = Utils.get_start_in_out_bound_suffix(route_id)
            result.append(str(route_id) + str(inbound_suffix))
            result.append(str(route_id) + str(outbound_suffix))
        return result
