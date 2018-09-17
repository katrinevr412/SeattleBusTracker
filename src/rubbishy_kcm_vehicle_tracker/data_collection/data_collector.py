from rubbishy_kcm_vehicle_tracker.client.kcm_api_client import KingCountyMetroRealTimeAPIClient
from rubbishy_kcm_vehicle_tracker.constants import Constants
from rubbishy_kcm_vehicle_tracker.utils.utils import Utils
from route_data_writer import RouteDataWriter
from vehicle_data_writer import VehicleDataWriter
from route_data_merger import RouteDataMerger
from vehicle_data_merger import VehicleDataMerger
from multiprocessing.pool import Pool
from functools import partial


def get_vehicle_from_routes(grouped_routes, data_collector):
    return data_collector.real_time_client.get_vehicle_info_on_routes(grouped_routes)


class DataCollector:

    def __init__(self):
        self.real_time_client = KingCountyMetroRealTimeAPIClient()
        self.route_data_writer = RouteDataWriter()
        self.vehicle_data_writer = VehicleDataWriter()
        self.route_data_merger = RouteDataMerger()
        self.vehicle_data_merger = VehicleDataMerger()

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        self.__init__()

    def collect(self):
        regrouped_routes = Utils.regroup(Constants.ALL_LINES)
        vehicles = []
        pool = Pool(len(regrouped_routes))
        results = pool.imap_unordered(
            partial(get_vehicle_from_routes, data_collector=self),
            regrouped_routes
        )
        for result in results:
            vehicles += result

        for vehicle in filter(lambda vehicle: len(str(vehicle.id)) >= 4, vehicles):
            self.route_data_writer.write_route(vehicle)
            self.vehicle_data_writer.write_vehicle(vehicle)

    def merge(self):
        """
            We merge temporary data from a particular day at 4AM every day.
            e.g. data points from 2018-11-20 04:00:00 to 2018-11-21 04:00:00 are considered data of date 2018.11.20
        :return:
        """
        self.route_data_merger.merge()
        self.vehicle_data_merger.merge()
