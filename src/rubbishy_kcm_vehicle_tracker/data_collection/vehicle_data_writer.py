from data_writer import DataWriter
from rubbishy_kcm_vehicle_tracker.common.project_path import ProjectPathConfig
import os


class VehicleDataWriter(DataWriter):

    def __init__(self):
        self.working_directory = os.path.join(
            ProjectPathConfig.SOURCE_ROOT_PATH,
            'data',
            'runtime',
            'temp',
            'vehicle'
        )
        DataWriter.__init__(self, self.working_directory)

    def write_vehicle(self, vehicle):
        self.write(str(vehicle.get_id()) + '.txt', vehicle.get_route_number() + ' ' + vehicle.get_line_name())
