from rubbishy_kcm_vehicle_tracker.kcm.client.kcm_api_client import KingCountyMetroRealTimeAPIClient
from rubbishy_kcm_vehicle_tracker.kcm.kcm_constants import KCMConstants
from rubbishy_kcm_vehicle_tracker.kcm.utils.kcm_utils import KCMUtils
from rubbishy_kcm_vehicle_tracker.one_bus_away.tracker.oba_tracker import OBATracker
from rubbishy_kcm_vehicle_tracker.common.global_constants import GlobalConstants
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
        self.oba_data_provider = OBATracker()
        self.route_data_writer = RouteDataWriter()
        self.vehicle_data_writer = VehicleDataWriter()
        self.route_data_merger = RouteDataMerger()
        self.vehicle_data_merger = VehicleDataMerger()

    def __getstate__(self):
        return {}

    def __setstate__(self, state):
        self.__init__()

    def collect(self, use_api=GlobalConstants.KCM_API):
        if use_api == GlobalConstants.KCM_API:
            vehicles = self.__get_kcm_vehicles()
        else:
            vehicles = self.__get_oba_vehicles()

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

    def __get_kcm_vehicles(self):
        regrouped_routes = KCMUtils.regroup(KCMConstants.ALL_LINES)
        vehicles = []
        pool = Pool(len(regrouped_routes))
        results = pool.imap_unordered(
            partial(get_vehicle_from_routes, data_collector=self),
            regrouped_routes
        )
        for result in results:
            vehicles += result
        return vehicles

    def __get_oba_vehicles(self):
        vehicles = self.oba_data_provider.get_vehicle_data(allow_bad_data=False)
        return vehicles
