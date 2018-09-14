from tracker_config import TrackerConfig
from vehicle_number_loader import VehicleNumberLoader
from utils import Utils
from constants import Constants
from route_info_proxy import RouteInfoProxy
from kcm_api_client import KingCountyMetroRealTimeAPIClient
from multiprocessing.pool import Pool
from functools import partial


def load_route_info(route_id, tracker):
    return route_id, \
           tracker.route_info_client.get_route_info([route_id],
                                                      cache=tracker.config.cache,
                                                      refresh_cache=tracker.config.refresh_cache)


def retrieve_vehicle_running_info(vehicle, route_dict):
    vehicle.get_vehicle_running_info(route_dict[str(vehicle.line_id)])
    return vehicle


class Tracker:

    def __init__(self):
        self.config = TrackerConfig()
        self.route_info_client = RouteInfoProxy()
        self.vehicle_info_client = KingCountyMetroRealTimeAPIClient()
        self.route_set = set()
        self.in_out_bound_route_dict = {}

    def track(self, cmd_str=''):
        if cmd_str.strip():
            # if inputted a command str, overwrite it
            self.config.cmd_str = cmd_str.strip()
        tracking_vehicle_set = VehicleNumberLoader().load(only_missing=self.config.missing_only)
        tracking_vehicle_routes = Utils.get_query_route_ids(cmd_str)
        tracking_routes = filter(lambda route_id: route_id not in self.route_set, tracking_vehicle_routes)
        result_vehicles = []
        if not self.config.enable_parallel:
            for route_id in tracking_routes:
                _, route_info = load_route_info(route_id, self)
                self.in_out_bound_route_dict.update(route_info)
                self.route_set.add(route_id)
        else:
            prc_pool = Pool(len(tracking_routes))
            results = prc_pool.imap_unordered(partial(load_route_info, tracker=self), tracking_routes)
            for route_id, route_info in results:
                self.in_out_bound_route_dict.update(route_info)
                self.route_set.add(route_id)

        # update vehicle for all routes in tracking_vehicle_routes
        grouped_tracking_vehicle_routes = self.__regroup(tracking_vehicle_routes)
        output_results = []
        for route_ids in grouped_tracking_vehicle_routes:
            vehicles = self.vehicle_info_client.get_vehicle_info_on_routes(route_ids)
            result_vehicles += filter(lambda vehicle: str(vehicle.id) in tracking_vehicle_set, vehicles)
        if not self.config.enable_parallel:
            for vehicle in result_vehicles:
                vehicle.get_vehicle_running_info(self.in_out_bound_route_dict[str(vehicle.line_id)])
                output_results.append("%s" % vehicle)
        else:
            prc_pool = Pool(len(result_vehicles))
            results = prc_pool.imap_unordered(partial(retrieve_vehicle_running_info, route_dict=self.in_out_bound_route_dict), result_vehicles)
            for vehicle in results:
                output_results.append("%s" % vehicle)

        sorted_results = sorted(output_results)
        for result in sorted_results:
            print result

    def __regroup(self, tracking_routes, size=Constants.MAXIMUM_LINE_QUERY):
        grouped_routes = []
        temp_routes = []
        for i in range(len(tracking_routes)):
            if i % size == 0:
                if temp_routes:
                    grouped_routes.append(temp_routes)
                    temp_routes = []
            temp_routes.append(tracking_routes[i])
        if temp_routes:
            grouped_routes.append(temp_routes)
        return grouped_routes
