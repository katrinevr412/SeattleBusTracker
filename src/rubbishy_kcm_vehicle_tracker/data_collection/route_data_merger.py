from data_merger import DataMerger
from formatters import Formatters
import os


class RouteDataMerger(DataMerger):

    def __init__(self):
        from_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'runtime',
            'temp',
            'route'
        )
        to_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
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
