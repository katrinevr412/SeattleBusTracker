from tracker import Tracker
from constants import Constants
import re


def main():
    tracker = Tracker()
    while True:
        cmd_str = raw_input("Input the bases you want to track (c, n, e, s), or routes separated by space. Enter q to exit.")
        if re.match('^[cnes]+$', cmd_str):
            tracker.track_missing_vehicle(cmd_str=cmd_str)
        elif re.match('^[0-9 ]+$', cmd_str):
            tracker.track_by_route(
                filter(
                    lambda route_id: route_id.isdigit() and int(route_id) in Constants.ALL_LINES,
                    cmd_str.split(' ')
                )
            )
        elif cmd_str.strip() in ['q', 'exit']:
            break
        else:
            print 'Input is invalid, please try again.'


if __name__ == '__main__':
    main()
