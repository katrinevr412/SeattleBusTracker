from rubbishy_kcm_vehicle_tracker.one_bus_away.client.oba_real_time_api_client import OneBusAwayRealTimeAPIClient
from rubbishy_kcm_vehicle_tracker.one_bus_away.client.oba_real_time_api_client_exception import OneBusAwayRealTimeAPIClientException
from rubbishy_kcm_vehicle_tracker.one_bus_away.oba_constants import OBAConstants
from rubbishy_kcm_vehicle_tracker.one_bus_away.components.oba_route import OBARoute
from rubbishy_kcm_vehicle_tracker.one_bus_away.components.oba_position import OBAPosition
from rubbishy_kcm_vehicle_tracker.one_bus_away.components.oba_stop import OBAStop
from rubbishy_kcm_vehicle_tracker.one_bus_away.components.oba_vehicle import OBAVehicle
from oba_vehicle_id_parser import OBAVehicleIDParser
import httplib


class OBATrackingManager:

    def __init__(self):
        self.oba_route_id_map = {}
        self.raw_route_id_map = {}
        self.oba_client = OneBusAwayRealTimeAPIClient()

    def get_all_routes(self):
        if self.oba_route_id_map:
            return self.oba_route_id_map, self.raw_route_id_map
        result = {}
        for agency_id in OBAConstants.TRACKING_AGENCIES:
            route_data = self.oba_client.get_all_route_for_agency(agency_id)
            for jobj in route_data['data']['list']:
                oba_route = OBARoute.from_json_obj(jobj)
                if oba_route.is_valid():
                    result[oba_route.id] = oba_route
        self.oba_route_id_map = result
        for oba_route_id in result:
            route = result[oba_route_id]
            raw_id = route.get_plain_route_number()
            self.raw_route_id_map[raw_id] = route
        return result, self.raw_route_id_map

    def reload_route_cache(self):
        self.oba_client.oba_route_cache.clear()
        self.get_all_routes()

    def get_vehicle_status_from_raw_vehicle_id(self, raw_vehicle_id):
        result = []
        possible_vehicle_ids = OBAVehicleIDParser().parse(raw_vehicle_id)
        for vehicle_id in possible_vehicle_ids:
            vehicle = self.__get_vehicle_status(vehicle_id)
            if vehicle:
                result.append(vehicle)
        return result

    def __get_vehicle_status(self, vehicle_id):
        vehicle = OBAVehicle()
        try:
            json_obj = self.oba_client.get_vehicle_status(vehicle_id)
        except OneBusAwayRealTimeAPIClientException as e:
            self.__handle_api_exception(e)
            return None
        try:
            reference_obj = json_obj['data']['references']
            status_obj = json_obj['data']['entry']['status']
            if not status_obj:
                return None
            return self.__get_vehicle_from_status_and_reference(
                status_obj=status_obj,
                reference_obj=reference_obj
            )
        except KeyError:
            # if the JSON is invalid, it's corrupted data and we return nothing.
            return None

    def get_vehicles_on_route(self, raw_route_id):
        raw_route_id = raw_route_id.upper()
        raw_route_map = self.get_all_routes()[1]
        if not raw_route_id in raw_route_map:
            return []
        route = raw_route_map[raw_route_id]
        try:
            json_obj = self.oba_client.get_vehicles_on_route(route.id)
        except OneBusAwayRealTimeAPIClientException as e:
            self.__handle_api_exception(e)
            return []
        vehicles = []
        reference_obj = json_obj['data']['references']
        for result in json_obj['data']['list']:
            vehicles.append(
                self.__get_vehicle_from_status_and_reference(
                    status_obj=result['status'],
                    reference_obj=reference_obj
                )
            )
        return filter(lambda vehicle: vehicle.id and vehicle.route.id == route.id, vehicles)

    def get_running_vehicles_for_agency(self, agency_id):
        if not agency_id in OBAConstants.TRACKING_AGENCIES:
            return []
        try:
            json_obj = self.oba_client.get_vehicles_for_agency(agency_id=agency_id)
        except OneBusAwayRealTimeAPIClientException as e:
            self.__handle_api_exception(e)
            return []
        vehicles = []
        trips = filter(
            lambda trip: trip['tripId'] and trip['tripStatus'],
            json_obj['data']['list']
        )
        reference_obj = json_obj['data']['references']
        for result in trips:
            status_obj = result['tripStatus']
            vehicles.append(
                self.__get_vehicle_from_status_and_reference(status_obj, reference_obj)
            )
        return vehicles

    def __get_vehicle_from_status_and_reference(self, status_obj, reference_obj):
        vehicle_id = status_obj['vehicleId']
        trip_id = status_obj['activeTripId']
        next_stop_id = status_obj['nextStop']
        stop_map, route_map, head_sign_map = self.__get_stop_route_head_sign_maps_from_reference(reference_obj)
        route_id = route_map.get(trip_id)
        return OBAVehicle(
            id=vehicle_id,
            position=self.__get_position_from_status(status_obj),
            head_sign=head_sign_map.get(trip_id),
            next_stop=stop_map.get(next_stop_id),
            route=self.get_all_routes()[0].get(route_id) or OBARoute.from_route_id(route_id)
        )

    def __get_position_from_status(self, status_obj):
        return OBAPosition(
            long=status_obj['position']['lon'],
            lat=status_obj['position']['lat']
        )

    def __get_stop_route_head_sign_maps_from_reference(self, reference_obj):
        related_trips = reference_obj['trips']
        related_stops = reference_obj['stops']
        stop_map = {}
        head_sign_map = {}
        route_map = {}
        for trip in related_trips:
            head_sign_map[trip['id']] = trip['tripHeadsign']
            route_map[trip['id']] = trip['routeId']
        for stop in related_stops:
            stop_map[stop['id']] = OBAStop.from_json_obj(stop)
        return stop_map, route_map, head_sign_map

    def __handle_api_exception(self, api_exception, verbose=False):
        # if there is a 404, it means that the vehicle is currently not active.
        # otherwise, it's a real error
        if api_exception.status_code != httplib.NOT_FOUND:
            raise api_exception
        if verbose:
            print api_exception
        return
