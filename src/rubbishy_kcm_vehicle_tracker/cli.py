import sys
import os
import argparse
root_package_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, root_package_path)
from core.tracker import Tracker
from cache.cache_checker import CacheChecker
from cache.cache_loader import CacheLoader
from data_collection.data_collector import DataCollector


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='The operation to execute.', dest='operation')

    track_parser = subparsers.add_parser('track', help='Track the buses through base or routes.')
    track_by_group = track_parser.add_mutually_exclusive_group()
    track_by_group.add_argument('-base', '--base', type=str,
                                help='A command string showing the bases to track. C-central, N-north, E-east, S-south.'
                                                 'They can be combined to track multiple bases, e.g. CNS')
    track_by_group.add_argument('-routes', '--routes', nargs='*',
                                help='A list of routes separated by spaces.')
    track_parser.add_argument('-no-cache', '--cache', action='store_false', default=True,
                              help='Whether to use local route cache.')
    track_parser.add_argument('-refresh-cache', '--refresh_cache', action='store_true', default=False,
                              help='Whether to refresh local route cache.')
    track_parser.add_argument('-no-parallel', '--parallel', action='store_false', default=True,
                              help='Whether to enable parallel execution for API calls.')
    track_parser.add_argument('-missing-only', '--missing_only', action='store_true', default=False,
                              help='Whether to include only the missing vehicles (only valid for base mode)')

    cache_check_parser = subparsers.add_parser('cache-check', help='Cache checking tool for route stops.')
    cache_check_parser.add_argument('-delete', '--delete', action='store_true', default=False,
                                    help='Whether to delete the bad cache files after check.')

    cache_reload_parser = subparsers.add_parser('cache-reload', help='Force cache reload for route stops.')
    cache_reload_parser.add_argument('-no-parallel', '--parallel', action='store_false', default=True,
                                     help='Whether to enable parallel execution for API calls.')

    data_collection_parser = subparsers.add_parser('data-collect')
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
    tracker = Tracker(
        cache=args.cache,
        refresh_cache=args.refresh_cache,
        enable_parallel=args.parallel,
        missing_only=args.missing_only
    )
    if args.base:
        tracker.track_missing_vehicle(cmd_str=args.base.lower())
    elif args.routes:
        tracker.track_by_route(args.routes)


def handle_cache_check(args):
    CacheChecker().check(delete=args.delete)


def handle_cache_reload(args):
    CacheLoader().load(parallel=args.parallel)


def handle_data_collect(args):
    data_collector = DataCollector()
    data_collector.collect()


def handle_data_merge(args):
    data_collector = DataCollector()
    data_collector.merge()


if __name__ == '__main__':
    main()
