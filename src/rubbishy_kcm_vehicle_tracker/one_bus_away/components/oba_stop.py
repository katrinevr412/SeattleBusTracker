from oba_position import OBAPosition
from rubbishy_kcm_vehicle_tracker.one_bus_away.oba_constants import OBAConstants


class OBAStop:

    def __init__(self,
                 position=OBAPosition(),
                 id='1_23333',
                 code=OBAConstants.UNKNOWN,
                 name=OBAConstants.UNKNOWN):
        self.position = position
        self.id = id
        self.code = code
        self.name = name

    def distance_in_mile(self, position):
        return self.position.distance_in_mile(position)

    def __str__(self):
        return "%s (%s)" % (self.name, self.code)

    @staticmethod
    def from_json_obj(json_obj):
        oba_stop = OBAStop()
        oba_stop.position = OBAPosition(
            long=json_obj['lon'],
            lat=json_obj['lat']
        )
        oba_stop.id = json_obj['id']
        oba_stop.code = json_obj['code']
        oba_stop.name = json_obj['name']
        return oba_stop
