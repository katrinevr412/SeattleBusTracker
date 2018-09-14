import Queue


class Route:

    def __init__(self, id, stops, patterns):
        self.stops = stops
        self.patterns = patterns
        self.id = id

    def get_adjacent_stops(self, position):
        """
            Get the nearest stops of the current position.
        :param position:
        :return:
        """
        class ComparableStop:
            def __init__(self, stop, position):
                self.stop = stop
                self.position = position

            def __cmp__(self, other):
                return cmp(self.stop.distance_in_mile(position), other.stop.distance_in_mile(position))

        stop_priority_queue = Queue.PriorityQueue()
        for stop in self.stops:
            stop_priority_queue.put(ComparableStop(stop, position))

        pattern = None
        for pattern_ in self.patterns:
            if pattern_.contains(position):
                # TODO: we lazily load pattern. If we find a pattern we jump out immediately.
                pattern = pattern_
                break

        if not pattern:
            # if the position is not on any pattern, pop out the first and second stops and return
            return [stop_priority_queue.get().stop, stop_priority_queue.get().stop]

        all_stops = []
        acceptable_stops = []
        while not stop_priority_queue.empty():
            # we check each stop from distance nearest to the furthest. If a stop is acceptable, record it.
            # if there is no acceptable stop interval (i.e. two acceptable stops), just return the two nearest stops.
            next_popped_stop = stop_priority_queue.get().stop
            if len(all_stops) < 2:
                all_stops.append(next_popped_stop)
            if pattern.contains(next_popped_stop.position):
                acceptable_stops.append((next_popped_stop))
            if len(acceptable_stops) == 2:
                break
        if len(acceptable_stops) < 2:
            return all_stops[:2]
        return acceptable_stops[:2]
