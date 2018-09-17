import Queue
from math import pi as PI
from vector_utils import VectorUtils


class Route:

    STOP_PASS_ANGLE = PI / 3.0  # use 60 degree as a sanity check of whether the stop has passed.

    class ComparableStop:
        def __init__(self, stop, position):
            self.stop = stop
            self.position = position

        def __cmp__(self, other):
            return cmp(self.stop.distance_in_mile(self.position), other.stop.distance_in_mile(self.position))

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

        stop_priority_queue = Queue.PriorityQueue()
        for stop in self.stops:
            stop_priority_queue.put(Route.ComparableStop(stop, position))

        pattern = None
        for pattern_ in self.patterns:
            if pattern_.contains(position):
                # TODO: we lazily load pattern. If we find a pattern we jump out immediately.
                pattern = pattern_
                break

        if not pattern:
            # if the position is not on any pattern, pop out the first and second stops and return
            return self.__get_nearest_stops_with_condition(stop_priority_queue, position, lambda astop: True)

        return self.__get_nearest_stops_with_condition(stop_priority_queue, position, lambda astop: pattern.contains(astop.position))

    def __is_on_different_side(self, position, stop1, stop2):
        return VectorUtils.get_angle(
            position.get_relative_position(stop1.position),
            position.get_relative_position(stop2.position)
        ) >= self.STOP_PASS_ANGLE

    def __get_nearest_stops_with_condition(self, queue, position, condition):
        """
            Get the nearest stops for with the condition holds.
        :param condition:
        :return:
        """
        nearest_stop = None
        second_nearest_stop = None
        satisfy_condition_nearest_stop = None
        satisfy_condition_second_nearest_stop = None
        fallback_nearest = []
        while not queue.empty():
            popped_stop = queue.get().stop
            if len(fallback_nearest) < 2:
                fallback_nearest.append(popped_stop)
            if condition(popped_stop):
                if not satisfy_condition_nearest_stop:
                    satisfy_condition_nearest_stop = popped_stop
                elif not satisfy_condition_second_nearest_stop:
                    if self.__is_on_different_side(position, satisfy_condition_nearest_stop, popped_stop):
                        satisfy_condition_second_nearest_stop = popped_stop
                if satisfy_condition_second_nearest_stop:
                    return [satisfy_condition_nearest_stop, satisfy_condition_second_nearest_stop]
            if not nearest_stop:
                nearest_stop = popped_stop
            elif not second_nearest_stop:
                if self.__is_on_different_side(position, nearest_stop, popped_stop):
                    second_nearest_stop = popped_stop
        if satisfy_condition_second_nearest_stop:
            return [satisfy_condition_nearest_stop, satisfy_condition_second_nearest_stop]
        elif second_nearest_stop:
            return [nearest_stop, second_nearest_stop]
        else:
            return fallback_nearest[:2]
