import datetime
import pytz
from rubbishy_kcm_vehicle_tracker.kcm.kcm_constants import KCMConstants


class KCMUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_query_route_ids(cmd_arr):
        should_query_route_ids = []
        cmd_arr = [cmd.lower() for cmd in cmd_arr]
        if KCMConstants.CENTRAL_BASE_LINE_INDICATOR in cmd_arr:
            should_query_route_ids += KCMConstants.CENTRAL_BASE_LINES
        if KCMConstants.EAST_BASE_LINE_INDICATOR in cmd_arr:
            should_query_route_ids += KCMConstants.EAST_BASE_LINES
        if KCMConstants.NORTH_BASE_LINE_INDICATOR in cmd_arr:
            should_query_route_ids += KCMConstants.NORTH_BASE_LINES
        if KCMConstants.SOUTH_BASE_LINE_INDICATOR in cmd_arr:
            should_query_route_ids += KCMConstants.SOUTH_BASE_LINES
        if not KCMUtils.__is_rush_hour():
            should_query_route_ids = filter(lambda route: route in set(KCMConstants.REGULAR_LINES), should_query_route_ids)
        return should_query_route_ids

    @staticmethod
    def __is_rush_hour():
        """
            If current day is not weekend and hour is between 4pm and 7pm,
            it is considered rush hours.
        :return:
        """
        now = datetime.datetime.now(pytz.timezone('America/Los_Angeles'))
        return now.weekday() < 5 and now.hour in range(16, 20)

    @staticmethod
    def get_running_agency(vehicle_id):
        if len(str(vehicle_id)) < 4:
            return KCMConstants.UNKNOWN
        return KCMConstants.KCM \
            if len(str(vehicle_id)) == 4 and not str(vehicle_id).startswith('9') \
            else KCMConstants.ST

    @staticmethod
    def get_start_in_out_bound_suffix(route_id):
        for suffix in KCMConstants.IN_OUT_BOUND_SUFFIX_MAPPING:
            if int(route_id) in KCMConstants.IN_OUT_BOUND_SUFFIX_MAPPING[suffix]:
                return suffix, suffix + 1
        return KCMConstants.DEFAULT_INBOUND_LINEID_SUFFIX, KCMConstants.DEFAULT_OUTBOUND_LINEID_SUFFIX

    @staticmethod
    def regroup(tracking_routes, size=KCMConstants.MAXIMUM_LINE_QUERY):
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
