from oba_position import OBAPosition
from oba_stop import OBAStop
from oba_route import OBARoute
from oba_utils import OBAUtils
from i_vehicle import IVehicle
import re


class OBAVehicle(IVehicle):

    def __init__(self,
                 id='1_2333',
                 position=OBAPosition(),
                 next_stop=OBAStop(),
                 head_sign='',
                 route=OBARoute()):
        IVehicle.__init__(self, id)
        self.position = position
        self.next_stop = next_stop
        self.head_sign = head_sign
        self.route = route

    def __str__(self):
        next_position_distance = self.next_stop.distance_in_mile(self.position) if self.next_stop else -1
        vehicle_id = OBAUtils.get_raw_vehicle_id_from_oba_style_vehicle_id(self.id)
        return "%s bus No. %s on route %s - %s\nNext stop: %s\nDistance: %.2f miles" % (
            OBAUtils.get_agency_name_from_vehicle_id(self.id),
            vehicle_id if re.match(r'^[0-9]+$', vehicle_id) else vehicle_id[1:],
            self.route.get_printed_number(),
            self.head_sign,
            self.next_stop,
            next_position_distance
        )

    def get_route_number(self):
        return self.route.get_plain_route_number()

    def get_id(self):
        return OBAUtils.get_raw_vehicle_id_from_oba_style_vehicle_id(self.id)

    def get_line_name(self):
        return "%s - %s" % (self.route.get_raw_number(), self.head_sign)
