import json
import requests
import httplib
from oba_real_time_api_client_exception import OneBusAwayRealTimeAPIClientException
from oba_constants import OBAConstants
from oba_route_cache import OBARouteCache
import time


class OneBusAwayRealTimeAPIClient:

    def __init__(self):
        self.oba_route_cache = OBARouteCache()

    KEY = 'f4e0e1da-9e1d-4bf7-aa6f-50d161a9b665'
    CALL_INTERVAL = 101  # call interval in millisecond
    ENDPOINT = 'http://api.pugetsound.onebusaway.org/api/where'

    def get_all_route_for_agency(self, agency_id, force_reload=False):
        try:
            if force_reload:
                raise Exception()
            json_obj = self.oba_route_cache.read(agency_id)
        except:
            json_obj = self.__call(
                path='routes-for-agency',
                obj_id=agency_id,
                params={}
            )
            self.oba_route_cache.write(agency_id, json_obj)
        return json_obj

    def get_vehicle_status(self, vehicle_id):
        return self.__call(
            path='trip-for-vehicle',
            obj_id=vehicle_id,
            params={'includeTrip': 'true'}
        )

    def get_vehicles_on_route(self, route_id):
        return self.__call(
            path='trips-for-route',
            obj_id=route_id,
            params={'includeStatus': 'true'}
        )

    def get_vehicles_for_agency(self, agency_id):
        return self.__call(
            path='vehicles-for-agency',
            obj_id=agency_id,
            params={'includeStatus': 'true'}
        )

    def __call(self, path, obj_id, params):
        """
            Each call should be separated at least 100ms.
        :param path:
        :param obj_id:
        :param params:
        :return:
        """
        response = requests.get(
            url=self.__prepare_url(path, obj_id, params)
        )
        time.sleep(OBAConstants.QUERY_INTERVAL)
        if response.status_code != httplib.OK:
            raise OneBusAwayRealTimeAPIClientException("OBA API failed. Reason: %s" % response.text,
                                                       status_code=response.status_code)
        elif not response.text.strip():
            raise OneBusAwayRealTimeAPIClientException("OBA API returned empty response",
                                                       status_code=httplib.NOT_FOUND)

        return json.loads(response.text)

    def __prepare_url(self, path, obj_id, params):
        base_url = "%s/%s/%s.json?key=%s" % (self.ENDPOINT, path, str(obj_id), self.KEY)
        for key in params:
            base_url += "&%s=%s" % (key, params[key])
        return base_url
