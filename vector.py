import math


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, radians):
        return Vector(self.x * math.cos(radians) - self.y * math.sin(radians),
                      self.x * math.sin(radians) + self.y * math.cos(radians))

    def norm(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if other is float:
            return Vector(self.x * other, self.y * other)
        elif other is Vector:
            return self.x * other.x + self.y * other.y
        else:
            raise Exception('Unsupported multiply operation!')

    def __div__(self, other):
        if other is float:
            return Vector(self.x / other, self.y / other)
        else:
            raise Exception('Unsupported divide operation!')

    def unit_vector(self):
        return self / self.norm()

    def get_tuple(self):
        return self.x, self.y
