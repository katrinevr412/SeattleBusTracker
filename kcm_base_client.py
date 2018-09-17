from stop import Stop
from pattern import Pattern
from route import Route
from constants import Constants


class KCMBaseClient:

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

    def __get_start_in_out_bound_suffix(self, route_id):
        for suffix in Constants.IN_OUT_BOUND_SUFFIX_MAPPING:
            if int(route_id) in Constants.IN_OUT_BOUND_SUFFIX_MAPPING[suffix]:
                return suffix, suffix + 1
        return Constants.DEFAULT_INBOUND_LINEID_SUFFIX, Constants.DEFAULT_OUTBOUND_LINEID_SUFFIX

    def _plug_in_in_out_bound(self, route_ids):
        result = []
        for route_id in route_ids:
            inbound_suffix, outbound_suffix = self.__get_start_in_out_bound_suffix(route_id)
            result.append(str(route_id) + str(inbound_suffix))
            result.append(str(route_id) + str(outbound_suffix))
        return result
