# import os
# import sys
# root_package_path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# sys.path.insert(0, root_package_path)
from kcm_tracker import KCMTracker
from oba_tracker import OBATracker
from global_constants import GlobalConstants
from tracker_config import TrackerConfig
from instructions import Instructions
from rubbishy_argument_parser import RubbishyArgumentParser


def main():
    tracker_config = welcome()
    while True:
        cmd = raw_input("> ")
        args = RubbishyArgumentParser(tracker_config.api).parse_argument(cmd)
        if not args:
            continue
        if args.is_empty():
            exit(0)
        if tracker_config.api == GlobalConstants.OBA_API:
            handle_oba_track(args, tracker_config)
        else:
            handle_kcm_track(args, tracker_config)


def welcome():
    print "Welcome to Katrina's rubbishy bus tracking tool. It is designed for Android users to " \
          "track buses in Seattle wherever they go."
    tracker_config = TrackerConfig()
    if not Instructions().print_instruction(tracker_config.api):
        exit(0)
    return tracker_config


def handle_oba_track(args, config):
    oba_tracker = OBATracker()
    if args.bases:
        oba_tracker.track_by_base(bases=args.bases,
                                  missing_only=config.missing_only,
                                  allow_bad_routes=args.allow_bad_routes)
    elif args.routes:
        oba_tracker.track_by_route(args.routes)
    elif args.vehicles:
        oba_tracker.track_by_vehicle_number(vehicle_numbers=args.vehicles,
                                            allow_bad_routes=args.allow_bad_routes)
    else:
        print "Command line is incorrect. Please try again."


def handle_kcm_track(args, config):
    tracker = KCMTracker(
        cache=config.cache,
        refresh_cache=config.refresh_cache,
        enable_parallel=config.enable_parallel,
        missing_only=config.missing_only
    )
    if args.bases:
        tracker.track_missing_vehicle(bases=args.bases)
    elif args.routes:
        tracker.track_by_route(args.routes)
    else:
        print "Vehicle ID tracking is not available for KCM API mode. Please use OBA API mode instead."


if __name__ == '__main__':
    main()
