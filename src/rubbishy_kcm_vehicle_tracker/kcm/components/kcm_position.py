from rubbishy_kcm_vehicle_tracker.common.utils.vector_utils import VectorUtils
import math


class KCMPosition:

    EARTH_RADIUS = 3959

    def __init__(self, long=233.333, lat=233.333):
        self.long = long
        self.lat = lat

    def distance_in_mile(self, another_position):
        return VectorUtils.length(self.get_relative_position(another_position))

    def get_vector(self):
        theta = self.lat / 180.0 * math.pi
        phi = self.long / 180.0 * math.pi
        sin_theta = math.sin(theta)
        x = self.EARTH_RADIUS * math.cos(phi) * sin_theta
        y = self.EARTH_RADIUS * math.sin(phi) * sin_theta
        z = self.EARTH_RADIUS * math.cos(theta)
        return (x, y, z)

    def get_relative_position(self, another_position):
        return VectorUtils.subtract(another_position.get_vector(), self.get_vector())
