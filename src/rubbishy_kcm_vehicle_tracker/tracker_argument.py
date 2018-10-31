class TrackerArgument:

    def __init__(self, bases=[], routes=[], vehicles=[], valid=False, allow_bad_routes=True):
        self.is_valid = valid
        self.bases = bases
        self.routes = routes
        self.vehicles = vehicles
        self.allow_bad_routes = allow_bad_routes

    def is_empty(self):
        return not self.bases and not self.routes and not self.vehicles

    def __nonzero__(self):
        return self.is_valid

    @staticmethod
    def from_bases(bases):
        return TrackerArgument(bases=bases, valid=True)

    @staticmethod
    def from_routes(routes):
        return TrackerArgument(routes=routes, valid=True)

    @staticmethod
    def from_vehicles(vehicles):
        return TrackerArgument(vehicles=vehicles, valid=True)

    @staticmethod
    def invalid(message='', suppressed=False):
        if not suppressed:
            if message:
                print message
            else:
                print "input is invalid. Please try again."
        return TrackerArgument(valid=False)

    @staticmethod
    def empty():
        return TrackerArgument(valid=True)

    @staticmethod
    def switch():
        return None
