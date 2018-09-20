from data_writer import DataWriter
from rubbishy_kcm_vehicle_tracker.common.project_path import ProjectPathConfig
import os


class RouteDataWriter(DataWriter):

    def __init__(self):
        self.working_directory = os.path.join(
            ProjectPathConfig.SOURCE_ROOT_PATH,
            'data',
            'runtime',
            'temp',
            'route'
        )
        DataWriter.__init__(self, self.working_directory)

    def write_route(self, vehicle):
        self.write(str(vehicle.get_route_number()) + '.txt', str(vehicle.get_id()))
