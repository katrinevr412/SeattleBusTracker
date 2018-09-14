from tracker import Tracker


def main():
    cmd_str = raw_input("Input the bases you want to track (c, n, e, s):")
    Tracker().track(cmd_str=cmd_str)


if __name__ == '__main__':
    main()
