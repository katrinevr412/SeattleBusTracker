from kcm_position import KCMPosition
from kcm_stop import KCMStop
from rubbishy_kcm_vehicle_tracker.kcm.utils.kcm_utils import KCMUtils
from rubbishy_kcm_vehicle_tracker.common.i_vehicle import IVehicle
from rubbishy_kcm_vehicle_tracker.kcm.kcm_constants import KCMConstants


class KCMVehicle(IVehicle):

    def __init__(self):
        # dedicate to retired KCM bus No. 2333
        IVehicle.__init__(self, '2333')
        self.number = '2333'
        self.line_id = '00'
        self.line_name = '0 - ' + KCMConstants.UNKNOWN
        self.position = KCMPosition()
        self.adjacent_stops = [KCMStop(), KCMStop()]

    @staticmethod
    def deserialize_from_json_obj(json_obj):
        vehicle = KCMVehicle()
        vehicle.number = json_obj['VehicleNumber']
        vehicle.id = str(json_obj['VehicleId'])
        vehicle.line_id = json_obj['LineDirId']
        vehicle.line_name = json_obj['Signage']
        vehicle.position = KCMPosition(long=json_obj['Lon'], lat=json_obj['Lat'])
        return vehicle

    def get_vehicle_running_info(self, route):
        self.adjacent_stops = route.get_adjacent_stops(self.position)

    def get_route_number(self):
        return str(self.line_id)[:-1]

    def get_id(self):
        return self.id

    def get_line_name(self):
        return self.line_name

    def __str__(self):
        return "%s bus No. %s on route %s\nBetween stops:\n%s [%.2f miles]\n%s [%.2f miles]" % \
               (KCMUtils.get_running_agency(self.id), self.id, self.line_name,
                self.adjacent_stops[0], self.adjacent_stops[0].distance_in_mile(self.position),
                self.adjacent_stops[1], self.adjacent_stops[1].distance_in_mile(self.position))
