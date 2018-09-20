import sys
import os
import argparse
root_package_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, root_package_path)
from rubbishy_kcm_vehicle_tracker.kcm.tracker.kcm_tracker import KCMTracker
from rubbishy_kcm_vehicle_tracker.one_bus_away.tracker.oba_tracker import OBATracker
from rubbishy_kcm_vehicle_tracker.one_bus_away.manager.oba_tracking_manager import OBATrackingManager
from rubbishy_kcm_vehicle_tracker.kcm.cache.kcm_cache_checker import KCMCacheChecker
from rubbishy_kcm_vehicle_tracker.kcm.cache.kcm_cache_loader import KCMCacheLoader
from data_collection.data_collector import DataCollector
from common.global_constants import GlobalConstants


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='The operation to execute.', dest='operation')

    track_parser = subparsers.add_parser('track', help='Track the buses through base or routes.')
    track_by_group = track_parser.add_mutually_exclusive_group()
    track_by_group.add_argument('-bases', '--bases', nargs='*',
                                help='A command string showing the bases to track. C-central, N-north, E-east, S-south.'
                                                 'They can be combined to track multiple bases, e.g. CNS')
    track_by_group.add_argument('-routes', '--routes', nargs='*',
                                help='A list of routes separated by spaces.')
    track_by_group.add_argument('-vehicles', '--vehicles', nargs='*', help='A list of vehicles separated by spaces.'
                                                                           'Only available in OBA mode.')
    track_parser.add_argument('-api', '--api', choices=GlobalConstants.ALL_SUPPORTED_APIS, default=GlobalConstants.OBA_API,
                              help='Choose which OBA to use: KingCountyMetro or OneBusAway.')
    track_parser.add_argument('-no-cache', '--cache', action='store_false', default=True,
                              help='Whether to use local route cache.')
    track_parser.add_argument('-refresh-cache', '--refresh_cache', action='store_true', default=False,
                              help='Whether to refresh local route cache.')
    track_parser.add_argument('-no-parallel', '--parallel', action='store_false', default=True,
                              help='Whether to enable parallel execution for API calls.')
    track_parser.add_argument('-missing-only', '--missing_only', action='store_true', default=False,
                              help='Whether to include only the missing vehicles (only valid for base mode)')
    track_parser.add_argument('-allow-bad-route', '--allow_bad_route', action='store_true', default=False,
                              help='Whether to include results where the route info is corrupted.')

    cache_check_parser = subparsers.add_parser('cache-check', help='Cache checking tool for route stops.')
    cache_check_parser.add_argument('-delete', '--delete', action='store_true', default=False,
                                    help='Whether to delete the bad cache files after check.')

    cache_reload_parser = subparsers.add_parser('cache-reload', help='Force cache reload for route stops.')
    cache_reload_parser.add_argument('-api', '--api', choices=GlobalConstants.ALL_SUPPORTED_APIS, default=GlobalConstants.OBA_API,
                                     help='The API the reloaded cache is related to.')
    cache_reload_parser.add_argument('-no-parallel', '--parallel', action='store_false', default=True,
                                     help='Whether to enable parallel execution for API calls.')

    data_collection_parser = subparsers.add_parser('data-collect')
    data_collection_parser.add_argument('-api', '--api', choices=GlobalConstants.ALL_SUPPORTED_APIS, default=GlobalConstants.OBA_API,
                                     help='The API to use to collect data.')

    data_merge_parser = subparsers.add_parser('data-merge')

    args = parser.parse_args()
    if args.operation == 'track':
        handle_track(args)
    elif args.operation == 'cache-check':
        handle_cache_check(args)
    elif args.operation == 'cache-reload':
        handle_cache_reload(args)
    elif args.operation == 'data-collect':
        handle_data_collect(args)
    elif args.operation == 'data-merge':
        handle_data_merge(args)


def handle_track(args):
    if args.api == GlobalConstants.KCM_API:
        tracker = KCMTracker(
            cache=args.cache,
            refresh_cache=args.refresh_cache,
            enable_parallel=args.parallel,
            missing_only=args.missing_only
        )
        if args.bases:
            tracker.track_missing_vehicle(bases=args.bases)
        elif args.routes:
            tracker.track_by_route(args.routes)
        else:
            print "Vehicle ID tracking is not available for KCM API mode. Please use OBA API mode instead."
    else:
        oba_tracker = OBATracker()
        if args.bases:
            oba_tracker.track_by_base(bases=args.bases,
                                      missing_only=args.missing_only,
                                      allow_bad_routes=args.allow_bad_route)
        elif args.routes:
            oba_tracker.track_by_route(args.routes)
        elif args.vehicles:
            oba_tracker.track_by_vehicle_number(vehicle_numbers=args.vehicles,
                                                allow_bad_routes=args.allow_bad_route)
        else:
            print "Command line is incorrect. Please try again."


def handle_cache_check(args):
    KCMCacheChecker().check(delete=args.delete)


def handle_cache_reload(args):
    if args.api == GlobalConstants.KCM_API:
        KCMCacheLoader().load(parallel=args.parallel)
    else:
        OBATrackingManager().reload_route_cache()


def handle_data_collect(args):
    data_collector = DataCollector()
    data_collector.collect(use_api=args.api)


def handle_data_merge(args):
    data_collector = DataCollector()
    data_collector.merge()


if __name__ == '__main__':
    main()
