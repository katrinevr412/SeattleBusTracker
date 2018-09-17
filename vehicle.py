from position import Position
from stop import Stop
from utils import Utils


class Vehicle:

    def __init__(self):
        # dedicate to retired KCM bus No. 2333
        self.number = '2333'
        self.id = '2333'
        self.line_id = '00'
        self.line_name = '0 - Unknown'
        self.position = Position()
        self.adjacent_stops = [Stop(), Stop()]

    @staticmethod
    def deserialize_from_json_obj(json_obj):
        vehicle = Vehicle()
        vehicle.number = json_obj['VehicleNumber']
        vehicle.id = str(json_obj['VehicleId'])
        vehicle.line_id = json_obj['LineDirId']
        vehicle.line_name = json_obj['Signage']
        vehicle.position = Position(long=json_obj['Lon'], lat=json_obj['Lat'])
        return vehicle

    def get_vehicle_running_info(self, route):
        self.adjacent_stops = route.get_adjacent_stops(self.position)

    def __str__(self):
        return "%s bus No. %s on route %s between stops %s [%.2f miles] and %s [%.2f miles]" % \
                (Utils.get_running_agency(self.id), self.id, self.line_name,
                 self.adjacent_stops[0], self.adjacent_stops[0].distance_in_mile(self.position),
                 self.adjacent_stops[1], self.adjacent_stops[1].distance_in_mile(self.position))
