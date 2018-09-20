from kcm_position import KCMPosition
from math import pi as PI
from rubbishy_kcm_vehicle_tracker.common.utils.vector_utils import VectorUtils


class KCMPattern:

    # we use 170 degrees angle formed by the position and two adjacent support points
    # in the pattern to decide whether the position is on the pattern.
    ON_ROUTE_ANGLE_THRESHOLD = 170 / 180.0 * PI

    def __init__(self, points=()):
        self.points = list(points)

    @staticmethod
    def deserialize_from_json_obj(json_obj):
        points = [KCMPosition(long=point['lon'], lat=point['lat']) for point in json_obj['Points']]
        return KCMPattern(points=points)

    def contains(self, position):
        """
            Determine whether this pattern contains a given position.
        :param position:
        :return:
        """
        for i in range(len(self.points) - 1):
            vec_first = position.get_relative_position(self.points[i])
            vec_second = position.get_relative_position(self.points[i+1])
            if VectorUtils.get_angle(vec_first, vec_second) >= KCMPattern.ON_ROUTE_ANGLE_THRESHOLD:
                return True
        return False
