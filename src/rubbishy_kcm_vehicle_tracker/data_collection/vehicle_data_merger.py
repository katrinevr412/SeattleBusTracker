from data_merger import DataMerger
from formatters import Formatters
import os


class VehicleDataMerger(DataMerger):

    def __init__(self):
        from_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'runtime',
            'temp',
            'vehicle'
        )
        to_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'runtime',
            'vehicle'
        )
        DataMerger.__init__(
            self,
            from_dir=from_dir,
            to_dir=to_dir,
            date_formatter=Formatters.date_formatter,
            file_formatter=Formatters.vehicle_file_formatter
        )
