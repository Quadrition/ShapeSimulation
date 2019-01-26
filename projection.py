class Projection:

    def __init__(self, max, min):
        self.max = max
        self.min = min

    def check_projection_overlap(self, projection):
        first_center = (self.max + self.min) / 2
        second_center = (projection.max + projection.min) / 2
        if first_center < second_center and self.max >= projection.min:
            return True
        elif second_center < first_center and self.min <= projection.max:
            return True
        elif first_center == second_center:
            return True
        return False

    def get_projection_overlap(self, projection):
        first_center = (self.max + self.min) / 2
        second_center = (projection.max + projection.min) / 2
        if first_center < second_center and self.max >= projection.min:
            if self.min >= projection.min:
                return abs(self.max - self.min)
            return abs(self.max - projection.min)
        elif second_center < first_center and projection.max >= self.min:
            if projection.min >= self.min:
                return abs(projection.max - projection.min)
            return abs(projection.max - self.min)
        elif first_center == second_center:
            if self.max > projection.max:
                return abs(projection.max - projection.min)
            return abs(self.max - self.min)
        return -1

    def find_middle_vertex(self, vertices):
        pass
