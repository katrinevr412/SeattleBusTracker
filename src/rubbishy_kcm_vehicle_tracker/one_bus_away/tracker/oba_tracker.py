from rubbishy_kcm_vehicle_tracker.one_bus_away.manager.oba_tracking_manager import OBATrackingManager
from rubbishy_kcm_vehicle_tracker.one_bus_away.oba_constants import OBAConstants
from rubbishy_kcm_vehicle_tracker.one_bus_away.utils.oba_utils import OBAUtils
from rubbishy_kcm_vehicle_tracker.common.vehicle_number_loader import VehicleNumberLoader


class OBATracker:

    def __init__(self):
        self.tracking_manager = OBATrackingManager()

    def track_by_route(self, routes):
        vehicles = []
        for route in routes:
            vehicles += self.tracking_manager.get_vehicles_on_route(route)
        self.__print_result(vehicles)

    def track_by_vehicle_number(self, vehicle_numbers, allow_bad_routes=False):
        vehicles = []
        for vehicle_number in vehicle_numbers:
            vehicles += self.tracking_manager.get_vehicle_status_from_raw_vehicle_id(vehicle_number)
        if not allow_bad_routes:
            vehicles = filter(
                lambda vehicle: vehicle.route.is_valid(),
                vehicles
            )
        self.__print_result(vehicles)

    def track_by_base(self, bases, missing_only=True, allow_bad_routes=False):
        should_include_routes = self.__get_included_routes_from_bases(bases)
        should_include_agencies = self.__get_included_agencies_from_bases(bases)
        tracking_vehicles = VehicleNumberLoader().load(missing_only=missing_only)
        vehicles = []
        for agency in should_include_agencies:
            vehicles += self.tracking_manager.get_running_vehicles_for_agency(agency_id=agency)
        should_include_vehicles = filter(
            lambda vehicle: OBAUtils.get_raw_vehicle_id_from_oba_style_vehicle_id(vehicle.id) in tracking_vehicles
                                and
                            (
                                # we leave this outlet to discover bad routes (they might be newly added routes).
                                    vehicle.route.get_printed_number() in should_include_routes
                                    or
                                    (allow_bad_routes and not vehicle.route.is_valid())
                             ),
            vehicles
        )
        self.__print_result(should_include_vehicles)

    def get_vehicle_data(self, allow_bad_data=False):
        vehicles = []
        for agency in OBAConstants.TRACKING_AGENCIES:
            vehicles += self.tracking_manager.get_running_vehicles_for_agency(agency_id=agency)
        return filter(
            lambda vehicle: allow_bad_data or vehicle.route.is_valid(),
            vehicles
        )

    def __print_result(self, results):
        if not results:
            print "No result found.\n"
            return
        print "%d results found:\n" % len(results)
        printed = []
        for result in results:
            printed.append("%s" % result)
        for printed_reesult in sorted(printed):
            print printed_reesult + '\n'

    def __get_included_routes_from_bases(self, bases):
        routes = []
        for base in bases:
            if base not in OBAConstants.TRACKING_LINES_FOR_BASES:
                continue
            routes += OBAConstants.TRACKING_LINES_FOR_BASES[base]
        return list(set(routes))

    def __get_included_agencies_from_bases(self, bases):
        agencies = []
        for base in bases:
            if base not in OBAConstants.TRACKING_AGENCIES_FOR_BASES:
                continue
            agencies += OBAConstants.TRACKING_AGENCIES_FOR_BASES[base]
        return list(set(agencies))
