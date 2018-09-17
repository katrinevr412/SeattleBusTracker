import datetime
import pytz
import os
from rubbishy_kcm_vehicle_tracker.constants import Constants


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def get_query_route_ids(cmd_str):
        should_query_route_ids = []
        cmd_str = cmd_str.lower()
        if 'c' in cmd_str:
            should_query_route_ids += Constants.CENTRAL_BASE_LINES
        if 'e' in cmd_str:
            should_query_route_ids += Constants.EAST_BASE_LINES
        if 'n' in cmd_str:
            should_query_route_ids += Constants.NORTH_BASE_LINES
        if 's' in cmd_str:
            should_query_route_ids += Constants.SOUTH_BASE_LINES
        if not Utils.__is_rush_hour():
            should_query_route_ids = filter(lambda route: route in set(Constants.REGULAR_LINES), should_query_route_ids)
        return should_query_route_ids

    @staticmethod
    def __is_rush_hour():
        """
            If current day is not weekend and hour is between 4pm and 7pm,
            it is considered rush hours.
        :return:
        """
        now = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
        return now.weekday() < 5 and now.hour in range(16, 19)

    @staticmethod
    def get_running_agency(vehicle_id):
        # TODO: add Pierce Transit and Community Transit into this logic
        if len(str(vehicle_id)) < 4:
            return 'Unknown'
        return "KingCountyMetro" \
            if len(str(vehicle_id)) == 4 and not str(vehicle_id).startswith('9') \
            else "SoundTransit"

    @staticmethod
    def get_start_in_out_bound_suffix(route_id):
        for suffix in Constants.IN_OUT_BOUND_SUFFIX_MAPPING:
            if int(route_id) in Constants.IN_OUT_BOUND_SUFFIX_MAPPING[suffix]:
                return suffix, suffix + 1
        return Constants.DEFAULT_INBOUND_LINEID_SUFFIX, Constants.DEFAULT_OUTBOUND_LINEID_SUFFIX

    @staticmethod
    def regroup(tracking_routes, size=Constants.MAXIMUM_LINE_QUERY):
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

    @staticmethod
    def make_dir_if_not_exists(dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
