from rubbishy_kcm_vehicle_tracker.kcm.components.kcm_stop import KCMStop
from rubbishy_kcm_vehicle_tracker.kcm.components.kcm_pattern import KCMPattern
from rubbishy_kcm_vehicle_tracker.kcm.components.kcm_route import KCMRoute
from rubbishy_kcm_vehicle_tracker.kcm.cache.kcm_route_info_cache import KCMRouteInfoCache
from rubbishy_kcm_vehicle_tracker.kcm.utils.kcm_utils import KCMUtils


class KCMBaseClient:

    def __init__(self):
        self.cache_client = KCMRouteInfoCache()

    def _process_route_response(self, result):
        res = {}
        for route_id in result:
            response_data = result[route_id]
            stops = response_data['result']['stops']
            patterns = response_data['result']['lineTraces']['patternTraces']
            res[route_id] = KCMRoute(route_id,
                                     [KCMStop.deserialize_from_json_obj(stop) for stop in stops],
                                     [KCMPattern.deserialize_from_json_obj(pattern) for pattern in patterns])
        return res

    def _plug_in_in_out_bound(self, route_ids):
        result = []
        for route_id in route_ids:
            inbound_suffix, outbound_suffix = KCMUtils.get_start_in_out_bound_suffix(route_id)
            result.append(str(route_id) + str(inbound_suffix))
            result.append(str(route_id) + str(outbound_suffix))
        return result
