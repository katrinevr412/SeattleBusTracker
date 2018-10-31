from tracker_argument import TrackerArgument
from global_constants import GlobalConstants
from oba_constants import OBAConstants
from kcm_constants import KCMConstants
import re


class RubbishyArgumentParser:

    ROUTE_PATTERN = re.compile(r'^[CP]?[0-9]{1,3}$')
    VEHICLE_PATTERN = re.compile(r'^[CP]?[0-9]{3,5}$')

    def __init__(self, api):
        self.api = api

    def parse_argument(self, cmd_line):
        cmd_arr = cmd_line.split()
        if not cmd_arr:
            # empty command
            return TrackerArgument.invalid()
        type_cmd = cmd_arr[0].lower()
        if type_cmd in GlobalConstants.EXIT_COMMANDS:
            # exit command
            return TrackerArgument.empty()
        elif type_cmd == GlobalConstants.SWITCH_API_COMMAND:
            # switch API command
            return TrackerArgument.switch()
        elif type_cmd == GlobalConstants.BASE_COMMAND:
            # explicit base command
            return self.__parse_base_command(cmd_arr[1:])
        elif type_cmd == GlobalConstants.ROUTE_COMMAND:
            # explicit route command
            return self.__parse_route_command(cmd_arr[1:])
        elif type_cmd == GlobalConstants.VEHICLE_COMMAND:
            # explicit vehicle command (vehicle tracking must be explicit)
            return self.__parse_vehicle_command(cmd_arr[1:])
        else:
            # implicits
            return self.__parse_base_command(cmd_arr, suppressed=True) or self.__parse_route_command(cmd_arr)

    def __parse_base_command(self, cmd_arr, suppressed=False):
        if not self.__is_base_command(cmd_arr):
            return TrackerArgument.invalid(suppressed=suppressed)
        return TrackerArgument.from_bases([x.lower() for x in cmd_arr])

    def __parse_route_command(self, cmd_arr):
        if not self.__is_route_command(cmd_arr):
            return TrackerArgument.invalid()
        return TrackerArgument.from_routes([x.upper() for x in cmd_arr])

    def __parse_vehicle_command(self, cmd_arr):
        if not self.__is_vehicle_command(cmd_arr):
            return TrackerArgument.invalid()
        return TrackerArgument.from_vehicles([x.upper() for x in cmd_arr])

    def __is_base_command(self, cmd_arr):
        valid_base_list = OBAConstants.TRACKING_LINES_FOR_BASES \
            if self.api == GlobalConstants.OBA_API \
            else KCMConstants.ALL_VALID_TRACKING_BASES
        return filter(
            lambda x: x.lower() in valid_base_list,
            cmd_arr
        )

    def __is_route_command(self, cmd_arr):
        return filter(
            lambda x: self.ROUTE_PATTERN.match(x.upper()),
            cmd_arr
        )

    def __is_vehicle_command(self, cmd_arr):
        if len(cmd_arr) > GlobalConstants.VEHICLE_COMMAND_LIMIT:
            return TrackerArgument.invalid("Cannot track more than %s vehicles at once." % GlobalConstants.VEHICLE_COMMAND_LIMIT)
        return filter(
            lambda x: self.VEHICLE_PATTERN.match(x.upper()),
            cmd_arr
        )
