from tracker import Tracker
from constants import Constants
import re


def main():
    cmd_str = raw_input("Input the bases you want to track (c, n, e, s), or routes separated by space:")
    tracker = Tracker()
    if re.match('^[cnes]+$', cmd_str):
        tracker.track_missing_vehicle(cmd_str=cmd_str)
    else:
        tracker.track_by_route(
            filter(
                lambda route_id: route_id.isdigit() and int(route_id) in Constants.ALL_LINES,
                cmd_str.split(' ')
            )
        )


if __name__ == '__main__':
    main()
