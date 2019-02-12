import globals
import pygame


class QuadNode:
    def __init__(self, x_max, x_min, y_max, y_min):
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.shapes = []
        self.children = []

    def add_shape(self, shape):
        self.shapes.append(shape)
        if len(self.shapes) > globals.MAX_NODE_SHAPES:
            self.split()

    def is_fitting(self, shape):
        shape_borders = shape.borders
        if shape_borders[0] > self.x_max:
            return False
        if shape_borders[1] < self.x_min:
            return False
        if shape_borders[2] > self.y_max:
            return False
        if shape_borders[3] < self.y_min:
            return False
        return True

    def split(self):
        self.children.append(
            QuadNode((self.x_max + self.x_min) / 2, self.x_min, (self.y_max + self.y_min) / 2, self.y_min))
        self.children.append(
            QuadNode(self.x_max, (self.x_max + self.x_min) / 2, (self.y_max + self.y_min) / 2, self.y_min))
        self.children.append(
            QuadNode((self.x_max + self.x_min) / 2, self.x_min, self.y_max, (self.y_max + self.y_min) / 2))
        self.children.append(
            QuadNode(self.x_max, (self.x_max + self.x_min) / 2, self.y_max, (self.y_max + self.y_min) / 2))

        i = 0
        while i < len(self.shapes):
            for child in self.children:
                if child.is_fitting(self.shapes[i]):
                    child.add_shape(self.shapes[i])
                    del self.shapes[i]
                    i -= 1
                    break
            i += 1

    def get_node_shapes_collision(self):
        child_shapes = []
        nodes = self.children
        while len(nodes) != 0:
            new_nodes = []
            for node in nodes:
                child_shapes.extend(node.shapes)
                new_nodes.extend(node.children)
            nodes = new_nodes
        return [self.shapes, child_shapes]


class QuadTree:
    def __init__(self):
        self.root = QuadNode(globals.SCREEN_WIDTH, 0, globals.SCREEN_HEIGHT, 0)

    def add_shape(self, shape):
        nodes = [self.root]
        parent_node = self.root
        while len(nodes) != 0:
            found_node = None
            for node in nodes:
                if node.is_fitting(shape):
                    found_node = node
                    break
            if found_node is None:
                parent_node.add_shape(shape)
                break
            if len(found_node.children) == 0:
                found_node.add_shape(shape)
                break
            nodes = found_node.children
            parent_node = found_node

    def find_collision_points(self):
        collision = []
        nodes = [self.root]
        while len(nodes) != 0:
            new_nodes = []
            for node in nodes:
                if len(node.shapes) > 0:
                    collision.append(node.get_node_shapes_collision())
                new_nodes.extend(node.children)
            nodes = new_nodes
        return collision

    def draw_bars(self, win, node):
        if len(node.children) == 4:
            pygame.draw.line(win, (255, 255, 255), (node.children[0].x_max, node.children[0].y_min),
                             (node.children[2].x_max, node.children[2].y_max))
            pygame.draw.line(win, (255, 255, 255), (node.children[0].x_min, node.children[0].y_max),
                             (node.children[1].x_max, node.children[1].y_max))

            self.draw_bars(win, node.children[0])
            self.draw_bars(win, node.children[1])
            self.draw_bars(win, node.children[2])
            self.draw_bars(win, node.children[3])
