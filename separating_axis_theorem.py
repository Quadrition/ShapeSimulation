import numpy as np
from polygon import Polygon
from circle import Circle


def project_polygon_on_axis(polygon, axis):
    vertices = polygon.vertices
    min = float('inf')
    max = -float('inf')
    for i in range(len(vertices)):
        dot = round(np.dot(axis, vertices[i]), 2)
        if min > dot:
            min = dot
        if max < dot:
            max = dot
    return max, min


def project_circle_on_axis(circle, axis):
    max = np.dot((circle.centroid + axis * circle.radius), axis)
    min = np.dot((circle.centroid - axis * circle.radius), axis)
    if max < min:
        max, minimum = min, max
    return max, min


def get_polygon_axes(polygon):
    polygon.rotate_reference_vector(polygon.theta / 2)
    axes = []
    for i in range(polygon.degree):
        add = True
        axis = polygon.reference_vector / np.linalg.norm(polygon.reference_vector)
        for axe in axes:
            if np.array_equal(axis * -1, axe):
                add = False
                break
        if add:
            axes.append(axis)
        polygon.rotate_reference_vector(polygon.theta)
    polygon.rotate_reference_vector(-polygon.theta / 2)
    return axes


def get_projection_overlap(first_projection, second_projection):
    first_center = round((first_projection[0] + first_projection[1]) / 2, 2)
    second_center = round((second_projection[0] + second_projection[1]) / 2, 2)
    if first_center < second_center and round(first_projection[0], 2) >= round(second_projection[1], 2):
        if first_projection[1] >= second_projection[1]:
            return abs(first_projection[0] - first_projection[1])
        return abs(first_projection[0] - second_projection[1])
    elif second_center < first_center and round(second_projection[0], 2) >= round(first_projection[1], 2):
        if second_projection[1] >= first_projection[1]:
            return abs(second_projection[0] - second_projection[1])
        return abs(second_projection[0] - first_projection[1])
    elif first_center == round(second_center, 2):
        if first_projection[0] > second_projection[0]:
            return abs(second_projection[0] - second_projection[1])
        return abs(first_projection[0] - first_projection[1])
    return -1


def check_polygon_polygon_collision(first_polygon, second_polygon):
    first_axes = get_polygon_axes(first_polygon)
    second_axes = get_polygon_axes(second_polygon)
    minimum = float('inf')
    min_axis = None

    for axis in first_axes:
        first_projection = project_polygon_on_axis(first_polygon, axis)
        second_projection = project_polygon_on_axis(second_polygon, axis)
        overlap = get_projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return None
        elif minimum > overlap:
            minimum = overlap
            min_axis = axis

    for axis in second_axes:
        first_projection = project_polygon_on_axis(first_polygon, axis)
        second_projection = project_polygon_on_axis(second_polygon, axis)
        overlap = get_projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return None
        elif minimum > overlap:
            minimum = overlap
            min_axis = axis

    return min_axis


def check_circle_circle_collision(first_circle, second_circle):
    axis = second_circle.centroid - first_circle.centroid
    axis = axis / np.linalg.norm(axis)

    first_projection = project_circle_on_axis(first_circle, axis)
    second_projection = project_circle_on_axis(second_circle, axis)

    overlap = get_projection_overlap(first_projection, second_projection)
    if overlap == -1:
        return None

    return first_circle.centroid + axis * first_circle.radius


def check_polygon_circle_collision(polygon, circle):
    axes = get_polygon_axes(polygon)

    for axis in axes:
        first_projection = project_polygon_on_axis(polygon, axis)
        second_projection = project_circle_on_axis(circle, axis)
        if projection_overlap(first_projection, second_projection) == -1:
            return False

    return True


def find_polygon_collision_point(first_polygon, second_polygon, axis):
    first_min = float('inf')
    first_min_vertices = []
    first_max = -float('inf')
    first_max_vertices = []
    for vertex in first_polygon.vertices:
        dot = np.dot(vertex, axis)
        if round(first_min, 2) > round(dot, 2):
            first_min = dot
            first_min_vertices = [vertex]
        elif round(first_min, 2) == round(dot, 2):
            first_min_vertices.append(vertex)
        if round(first_max, 2) < round(dot, 2):
            first_max = dot
            first_max_vertices = [vertex]
        elif round(first_max, 2) == round(dot, 2):
            first_max_vertices.append(vertex)

    second_min = float('inf')
    second_min_vertices = []
    second_max = -float('inf')
    second_max_vertices = []
    for vertex in second_polygon.vertices:
        dot = np.dot(vertex, axis)
        if round(second_min, 2) > round(dot, 2):
            second_min = dot
            second_min_vertices = [vertex]
        elif round(second_min, 2) == round(dot, 2):
            second_min_vertices.append(vertex)
        if round(second_max, 2) < round(dot, 2):
            second_max = dot
            second_max_vertices = [vertex]
        elif round(second_max, 2) == round(dot, 2):
            second_max_vertices.append(vertex)

    if abs(first_max - second_min) < abs(first_min - second_max):
        first_vertices = first_max_vertices
        second_vertices = second_min_vertices
    else:
        first_vertices = first_min_vertices
        second_vertices = second_max_vertices

    if len(first_vertices) == 1:
        return first_vertices[0]
    elif len(second_vertices) == 1:
        return second_vertices[0]

    if np.sum(first_vertices[0]) < np.sum(first_vertices[1]):
        first_vertices[0], first_vertices[1] = first_vertices[1], first_vertices[0]
    if np.sum(second_vertices[0]) < np.sum(second_vertices[1]):
        second_vertices[0], second_vertices[1] = second_vertices[1], second_vertices[0]
    first_max = np.sum(first_vertices[0])
    first_min = np.sum(first_vertices[1])
    second_max = np.sum(second_vertices[0])
    second_min = np.sum(second_vertices[1])

    first_center = (first_max + first_min) / 2
    second_center = (second_max + second_min) / 2
    if first_center < second_center:
        if first_max >= second_max:
            return (second_vertices[0] + second_vertices[1]) / 2
        if first_min >= second_min:
            return (first_vertices[0] + first_vertices[1]) / 2
        return (first_vertices[0] + second_vertices[1]) / 2
    elif second_center < first_center:
        if first_min <= second_min:
            return (second_vertices[0] + second_vertices[1]) / 2
        if first_max <= second_max:
            return (first_vertices[0] + first_vertices[1]) / 2
        return (second_vertices[0] + first_vertices[1]) / 2
    elif first_center == second_center:
        if first_max >= second_max:
            return (second_vertices[0] + second_vertices[1]) / 2
        return (first_vertices[0] + first_vertices[1]) / 2


def check_shapes_collision(first_shape, second_shape):
    if isinstance(first_shape, Polygon) and isinstance(second_shape, Polygon):
        mtv = check_polygon_polygon_collision(first_shape, second_shape)
        if mtv is None:
            return mtv
        return find_polygon_collision_point(first_shape, second_shape, mtv)
    elif isinstance(first_shape, Polygon) and isinstance(second_shape, Circle):
        return check_polygon_circle_collision(first_shape, second_shape)
    elif isinstance(first_shape, Circle) and isinstance(second_shape, Polygon):
        return check_polygon_circle_collision(second_shape, first_shape)
    elif isinstance(first_shape, Circle) and isinstance(second_shape, Circle):
        return check_circle_circle_collision(first_shape, second_shape)
