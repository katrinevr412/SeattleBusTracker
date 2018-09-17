import datetime
import pytz
from constants import Constants


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
