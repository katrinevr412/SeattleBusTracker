from data_writer import DataWriter
import os


class VehicleDataWriter(DataWriter):

    def __init__(self):
        self.working_directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'runtime',
            'temp',
            'vehicle'
        )
        DataWriter.__init__(self, self.working_directory)

    def write_vehicle(self, vehicle):
        self.write(str(vehicle.id) + '.txt', vehicle.get_route_number() + ' ' + vehicle.line_name)
