from data_writer import DataWriter
import os


class RouteDataWriter(DataWriter):

    def __init__(self):
        self.working_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'runtime',
            'temp',
            'route'
        )
        DataWriter.__init__(self, self.working_directory)

    def write_route(self, vehicle):
        self.write(str(vehicle.get_route_number()) + '.txt', str(vehicle.id))
