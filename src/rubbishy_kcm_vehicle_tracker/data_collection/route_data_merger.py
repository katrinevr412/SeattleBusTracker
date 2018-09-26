from data_merger import DataMerger
from formatters import Formatters
from rubbishy_kcm_vehicle_tracker.common.project_path import ProjectPathConfig
import os


class RouteDataMerger(DataMerger):

    def __init__(self):
        from_dir = os.path.join(
            ProjectPathConfig.DATA_ROOT_PATH,
            'runtime',
            'temp',
            'route'
        )
        to_dir = os.path.join(
            ProjectPathConfig.DATA_ROOT_PATH,
            'runtime',
            'route'
        )
        DataMerger.__init__(
            self,
            from_dir=from_dir,
            to_dir=to_dir,
            date_formatter=Formatters.date_formatter,
            file_formatter=Formatters.route_file_formatter
        )
