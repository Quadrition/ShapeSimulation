import numpy as np
from polygon import Polygon
from circle import Circle


# Projects polygon on axis and returns maximum and minimum projection
def project_polygon_on_axis(polygon, axis):
    vertices = polygon.vertices
    minimum = float('inf')
    maximum = -float('inf')
    for i in range(len(vertices)):
        dot = np.dot(axis, vertices[i])
        if minimum > dot:
            minimum = dot
        if maximum < dot:
            maximum = dot
    return maximum, minimum


# Projects circle on axis and returns maximum and minimum projection
def project_circle_on_axis(circle, axis):
    maximum = np.dot((circle.centroid + axis * circle.radius), axis)
    minimum = np.dot((circle.centroid - axis * circle.radius), axis)
    if maximum < minimum:
        maximum, minimum = minimum, maximum
    return maximum, minimum


# Gets polygon axes
def get_polygon_axes(polygon):
    polygon.rotate(polygon.theta / 2)
    axes = []
    for i in range(polygon.degree):
        add = True
        axis = polygon.reference_vector / np.linalg.norm(polygon.reference_vector)
        # Checks if axis exists
        for axe in axes:
            if np.array_equal(np.round(axis * -1, 2), np.round(axe, 2)):
                add = False
                break
        if add:
            axes.append(axis)
        polygon.rotate(polygon.theta)
    polygon.rotate(-polygon.theta / 2)
    return axes


# Checks if projection overlaps, and returns overlap, otherwise -1
def get_projection_overlap(first_projection, second_projection):
    # Calculate center of projections
    first_center = (first_projection[0] + first_projection[1]) / 2
    second_center = (second_projection[0] + second_projection[1]) / 2
    # Checks if collision exists
    if first_center < second_center and first_projection[0] < second_projection[1]:
        return -1
    elif second_center < first_center and second_projection[0] < first_projection[1]:
        return -1
    # Finds distance between largest minimum and smallest maximum
    if first_projection[0] < second_projection[0]:
        maximum = first_projection[0]
    else:
        maximum = second_projection[0]
    if first_projection[1] > second_projection[1]:
        minimum = first_projection[1]
    else:
        minimum = second_projection[1]
    return abs(maximum - minimum)


# Checks if 2 polygons are in collision and returns a collision point and mtv, otherwise None
def check_polygon_polygon_collision(first_polygon, second_polygon):
    axes = get_polygon_axes(first_polygon)
    minimum = float('inf')
    min_axis = None
    # Finding best axis on first polygon
    for axis in axes:
        first_projection = project_polygon_on_axis(first_polygon, axis)
        second_projection = project_polygon_on_axis(second_polygon, axis)
        overlap = get_projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return None
        elif minimum > overlap:
            minimum = overlap
            min_axis = axis
    # Finding best axis on second polygon
    axes = get_polygon_axes(second_polygon)
    for axis in axes:
        first_projection = project_polygon_on_axis(first_polygon, axis)
        second_projection = project_polygon_on_axis(second_polygon, axis)
        overlap = get_projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return None
        elif minimum > overlap:
            minimum = overlap
            min_axis = axis
    # Flipping axis if it points from second to first polygon
    if np.linalg.norm((first_polygon.centroid + min_axis) - second_polygon.centroid) > np.linalg.norm(
            (first_polygon.centroid - min_axis) - second_polygon.centroid):
        min_axis = -min_axis

    contact_point = get_contact_point_polygon(first_polygon, second_polygon, min_axis)
    return contact_point, min_axis


def get_contact_point_polygon(first_polygon, second_polygon, axis):
    # Get points that are in lines collision
    first_vertices = get_max_vertices(first_polygon, axis)
    second_vertices = get_max_vertices(second_polygon, -axis)

    # If there are 3 vertices, return the one on the middle
    if len(first_vertices) == 1:
        return first_vertices[0]
    elif len(second_vertices) == 1:
        return second_vertices[0]

    # Find a middle of 2 internal points
    if np.sum(first_vertices[0]) < np.sum(second_vertices[0]):
        maximum = first_vertices[0]
    else:
        maximum = second_vertices[0]
    if np.sum(first_vertices[1]) > np.sum(second_vertices[1]):
        minimum = first_vertices[1]
    else:
        minimum = second_vertices[1]
    return (maximum + minimum) / 2


# Finds vertices that have max dot product on axis (axis must point from center of polygon)
def get_max_vertices(polygon, axis):
    maximum = -float('inf')
    max_vertices = []
    for vertex in polygon.vertices:
        dot = np.round(np.dot(vertex, axis), 2)
        if dot > maximum:
            maximum = dot
            max_vertices = [vertex]
        elif dot == maximum:
            # Since result will have 2 vertices, let first be max
            if np.sum(max_vertices[0]) < np.sum(vertex):
                max_vertices.insert(0, vertex)
            else:
                max_vertices.append(vertex)
    return max_vertices


# Checks if 2 circles are in collision, and returns a collision point and mtv
def check_circle_circle_collision(first_circle, second_circle):
    # Gets mtv - axis from first to second center of circle
    mtv = second_circle.centroid - first_circle.centroid
    mtv = mtv / np.linalg.norm(mtv)

    first_projection = project_circle_on_axis(first_circle, mtv)
    second_projection = project_circle_on_axis(second_circle, mtv)
    # Gets overlap
    overlap = get_projection_overlap(first_projection, second_projection)
    if overlap == -1:
        return None

    collision_point = first_circle.centroid + mtv * first_circle.radius
    return collision_point, mtv


# Checks if polygon and circle are in collision
def check_polygon_circle_collision(polygon, circle):
    minimum = float('inf')
    min_axis = None
    # Finds mtv in polygon
    for axis in get_polygon_axes(polygon):
        first_projection = project_polygon_on_axis(polygon, axis)
        second_projection = project_circle_on_axis(circle, axis)
        overlap = get_projection_overlap(first_projection, second_projection)
        if overlap == -1:
            return None
        elif minimum > overlap:
            minimum = overlap
            min_axis = axis
    # Flips axis if it points from circle to polygon
    if np.linalg.norm((polygon.centroid + min_axis) - circle.centroid) > np.linalg.norm(
            (polygon.centroid - min_axis) - circle.centroid):
        min_axis = -min_axis
    # Gets points on mtv's edge
    points = get_max_vertices(polygon, min_axis)
    # If there is only 1 point put it as closest
    if len(points) == 1:
        pp = points[0]
    else:
        # Vector that represents edge
        s1 = points[1] - points[0]
        d1 = circle.centroid - points[0]
        # Distance between first point and closest point
        pr1 = np.dot(s1 / np.linalg.norm(s1), d1)
        # Check if distance is beyond edge
        if pr1 < 0:
            pp = points[0]
        elif pr1 > np.linalg.norm(s1):
            pp = points[1]
        else:
            pp = points[0] + (s1 / np.linalg.norm(s1)) * pr1
    # Project circle and polygon on axis from closes point on polygon to center of circle
    axis = circle.centroid - pp
    axis = axis / np.linalg.norm(axis)
    first_projection = project_polygon_on_axis(polygon, axis)
    second_projection = project_circle_on_axis(circle, axis)
    overlap = get_projection_overlap(first_projection, second_projection)
    if overlap == -1:
        return None
    elif minimum > overlap:
        min_axis = axis

    return pp, min_axis


# Finds maximum dot product of vertices for polygon and axis. It should always return 2 vertices
def find_best_vertex(polygon, axis):
    maximum = -float('inf')
    max_vector = None
    for i in range(polygon.degree):
        dot = np.dot(polygon.reference_vector / np.linalg.norm(polygon.reference_vector), axis)
        if maximum < dot:
            maximum = dot
            max_vector = polygon.centroid + polygon.reference_vector
        polygon.rotate(polygon.theta)
    return max_vector


# Main function for shapes collision
def check_shapes_collision(first_shape, second_shape):
    if isinstance(first_shape, Polygon) and isinstance(second_shape, Polygon):
        return check_polygon_polygon_collision(first_shape, second_shape)
    elif isinstance(first_shape, Polygon) and isinstance(second_shape, Circle):
        return check_polygon_circle_collision(first_shape, second_shape)
    elif isinstance(first_shape, Circle) and isinstance(second_shape, Polygon):
        return check_polygon_circle_collision(second_shape, first_shape)
    elif isinstance(first_shape, Circle) and isinstance(second_shape, Circle):
        return check_circle_circle_collision(first_shape, second_shape)
