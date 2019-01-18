import numpy as np
from polygon import Polygon
from circle import Circle


def project_polygon_on_axis(polygon, axis):
    vertices = polygon.vertices
    projection = []
    for vertex in vertices:
        projection.append(np.dot(axis, vertex))
    return np.array(projection)


def project_circle_on_axis(circle, axis):
    first_vertex = circle.centroid + axis
    second_vertex = circle.centroid - axis
    projection = [np.dot(axis, first_vertex), np.dot(axis, second_vertex)]
    return np.array(projection)


def projection_overlap(first_projection, second_projection):
    first_center = (first_projection.max() + first_projection.min()) / 2
    second_center = (second_projection.max() + second_projection.min()) / 2
    if first_center < second_center and first_projection.max() >= second_projection.min():
        return abs(abs(first_projection.max()) - abs(second_projection.min()))
    elif second_center < first_center and first_projection.min() <= second_projection.max():
        return abs(abs(first_projection.min()) - abs(second_projection.max()))
    elif first_center == second_center:
        if first_projection.min() < second_projection.min():
            return abs(abs(second_projection.max()) - abs(second_projection.min()))
        else:
            return abs(abs(first_projection.max()) - abs(first_projection.min()))
    return -1


def get_polygon_axes(polygon):
    polygon.rotate_reference_vector(polygon.theta / 2)
    axes = []
    for i in range(polygon.degree - 1):
        axes.append(polygon.reference_vector / np.linalg.norm(polygon.reference_vector))
        polygon.rotate_reference_vector(polygon.theta)
    axes.append(polygon.reference_vector)
    polygon.rotate_reference_vector(polygon.theta / 2)
    return axes


def check_polygon_polygon_collision(first_polygon, second_polygon):
    first_axes = get_polygon_axes(first_polygon)
    second_axes = get_polygon_axes(second_polygon)
    minimum = float('inf')

    for axis in first_axes:
        first_projection = project_polygon_on_axis(first_polygon, axis)
        second_projection = project_polygon_on_axis(second_polygon, axis)
        overlap = projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return False
        elif minimum > overlap:
            minimum = overlap

    for axis in second_axes:
        first_projection = project_polygon_on_axis(first_polygon, axis)
        second_projection = project_polygon_on_axis(second_polygon, axis)
        overlap = projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return False
        elif minimum > overlap:
            minimum = overlap

    return minimum


def check_circle_circle_collision(first_circle, second_circle):
    axis = first_circle.centroid - second_circle.centroid

    first_projection = project_circle_on_axis(first_circle, axis)
    second_projection = project_circle_on_axis(second_circle, axis)

    if projection_overlap(first_projection, second_projection) == -1:
        return False
    return True


def check_polygon_circle_collision(polygon, circle):
    axes = get_polygon_axes(polygon)

    for axis in axes:
        first_projection = project_polygon_on_axis(polygon, axis)
        second_projection = project_circle_on_axis(circle, axis)
        if projection_overlap(first_projection, second_projection) == -1:
            return False

    return True


def check_shapes_collision(first_shape, second_shape):
    if isinstance(first_shape, Polygon) and isinstance(second_shape, Polygon):
        return check_polygon_polygon_collision(first_shape, second_shape)
    elif isinstance(first_shape, Polygon) and isinstance(second_shape, Circle):
        return check_polygon_circle_collision(first_shape, second_shape)
    elif isinstance(first_shape, Circle) and isinstance(second_shape, Polygon):
        return check_polygon_circle_collision(second_shape, first_shape)
    elif isinstance(first_shape, Circle) and isinstance(second_shape, Circle):
        return check_circle_circle_collision(first_shape, second_shape)
