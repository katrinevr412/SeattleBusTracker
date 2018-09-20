import requests
import json
from rubbishy_kcm_vehicle_tracker.kcm.components.kcm_vehicle import KCMVehicle
from kcm_base_client import KCMBaseClient
from rubbishy_kcm_vehicle_tracker.kcm.kcm_constants import KCMConstants


class KingCountyMetroRealTimeAPIClient(KCMBaseClient):

    def __init__(self):
        KCMBaseClient.__init__(self)
        self.endpoint = 'http://tripplanner.kingcounty.gov/RealTimeManager'

    def get_raw_route_info_response(self, route_ids):
        in_out_bound_route_ids = self._plug_in_in_out_bound(route_ids)
        result = {}
        for route_id_ in in_out_bound_route_ids:
            request_data = {
                "version": "1.1",
                "method": "GetLineTraceAndStops",
                "params": {
                    "LineDirId": int(route_id_)
                }
            }
            response_data = self.__call(request_data)
            result[route_id_] = response_data
        return result

    def get_route_info(self, route_ids, cache=True):
        in_out_bound_route_ids = self._plug_in_in_out_bound(route_ids)
        result = {}
        for route_id_ in in_out_bound_route_ids:
            request_data = {
                "version": "1.1",
                "method": "GetLineTraceAndStops",
                "params":{
                    "LineDirId": int(route_id_)
                }
            }
            response_data = self.__call(request_data)
            result[route_id_] = response_data
            if cache:
                self.cache_client.write(route_id_, response_data)
        return self._process_route_response(result)

    def get_vehicle_info_on_routes(self, route_ids):
        if len(route_ids) > KCMConstants.MAXIMUM_LINE_QUERY:
            raise Exception('A maximum of %d routes can be queried at once.' % KCMConstants.MAXIMUM_LINE_QUERY)
        request_data = {
            "version": "1.1",
            "method": "GetTravelPoints",
            "params": {
                "travelPointsReqs": [
                    {"lineDirId": route_id, "callingApp": "RMD"} for route_id in self._plug_in_in_out_bound(route_ids)
                ],
                "interval": 10
            }
        }
        response_data = self.__call(request_data)
        vehicles = response_data['result']['travelPoints']
        return [KCMVehicle.deserialize_from_json_obj(json_obj) for json_obj in vehicles]


    def __call(self, request_data):
        response = requests.post(
            url='http://tripplanner.kingcounty.gov/RealTimeManager',
            headers={
                'Host': 'tripplanner.kingcounty.gov',
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'Referer': 'http://tripplanner.kingcounty.gov/hiwire?.a=iRealTimeDisplay'
            },
            data=json.dumps(request_data),
            verify=False
        )
        if response.status_code != 200:
            raise Exception('KCM API failed with status code: %d, message: %s' % (response.status_code, response.text))
        try:
            return json.loads(response.text)
        except:
            raise Exception('KCM API returned nonsense response: %s' % response.text)
