from position import Position


class Stop:

    def __init__(self, id=0, name='unknown', position=Position(long=233.3333, lat=233.3333)):
        self.id = id
        self.name = name
        self.position = position

    @staticmethod
    def deserialize_from_json_obj(json_obj):
        stop = Stop()
        stop.id = json_obj['stopId']
        stop.name = json_obj['name']
        stop.position = Position(json_obj['point']['lon'], json_obj['point']['lat'])
        return stop

    def distance_in_mile(self, position):
        return self.position.distance_in_mile(position)


    def __str__(self):
        return "%s (%s)" % (self.name, self.id)
