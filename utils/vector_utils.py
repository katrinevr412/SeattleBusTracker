import math


class VectorUtils:
    """
        This class is written mainly because Andriod qpython's numpy support is rubbishy.
    """

    @staticmethod
    def get_angle(vector1, vector2):
        if VectorUtils.length(vector1) == 0 or VectorUtils.length(vector2) == 0:
            # we favour 180 degrees instead of 0 because we want to include an overlapping stop
            return math.pi
        return math.acos(min(1, max(-1, VectorUtils.dot(vector1, vector2) / VectorUtils.length(vector1) / VectorUtils.length(vector2))))

    @staticmethod
    def dot(vector1, vector2):
        res = 0.0
        for i in range(min(len(vector1), len(vector2))):
            res += vector1[i] * vector2[i]
        return res

    @staticmethod
    def length(vector):
        res = 0.0
        for i in range(len(vector)):
            res += vector[i] * vector[i]
        return math.sqrt(res)

    @staticmethod
    def subtract(vector1, vector2):
        dim = min(len(vector1), len(vector2))
        res = []
        for i in range(dim):
            res.append(vector1[i] - vector2[i])
        return res
