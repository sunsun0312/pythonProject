import re
from collections import defaultdict
from copy import deepcopy

# use re module to find different part of the information
# built a dictionary, merge them into this dict and return dict
def available_coloured_pieces(file):
    p = file.read()
    p = p.split('\n')
    pattern = 'M[\s]*(\d+[\s]+\d+)[\s]*L[\s]*(.*)[\s]*z[\s]*"[\s]*fill[\s]*=[\s]*"(.+)"'
    each_piece = defaultdict(list)
    for line in p:
        match = re.search(pattern, line)
        if match:
            each_piece[match.group(3)].append([int(i) for i in match.group(1).split()])
            l = match.group(2).split('L')
            for i in l:
                each_piece[match.group(3)].append([int(j) for j in i.split()])
        else:
            match = re.search('M[\s]*(\d+[\s]+\d+)[\s]*z[\s]*"[\s]*fill[\s]*=[\s]*"(.+)"', line)
            if match:
                each_piece[match.group(2)].append([int(j) for j in match.group(1).split()])
    return each_piece

# assess whether every piece is valid
# if dict is empty, return false
# use cross product to assess whether it is cross or not convex
def are_valid(piece):
    # if not piece:
    #     return False
    for colour in piece:
        if len(set(tuple(i) for i in piece[colour])) != len(piece[colour]):
            return False
        point = piece[colour]
        if len(point) <= 2:
            return False
        else:
            for i in range(len(point) - 1):
                p1 = point[i:] + point[: i]
                p1_orientation = ((p1[1][0] - p1[0][0]) * (p1[2][1] - p1[0][1])) - (
                            (p1[2][0] - p1[0][0]) * (p1[1][1] - p1[0][1]))
                p2 = point[i + 1:] + point[: i + 1]
                p2_orientation = ((p2[1][0] - p2[0][0]) * (p2[2][1] - p2[0][1])) - (
                            (p2[2][0] - p2[0][0]) * (p2[1][1] - p2[0][1]))
                if not p1_orientation or not p2_orientation:
                    return False
                elif (p1_orientation > 0) != (p2_orientation > 0):
                    return False
                if len(point) > 3:
                    for j in range(3, len(point)):
                        p3_orientation = ((p1[1][0] - p1[0][0]) * (p1[j][1] - p1[0][1])) - \
                                         ((p1[j][0] - p1[0][0]) * (p1[1][1] - p1[0][1]))
                        if (p1_orientation > 0) != (p3_orientation > 0):
                            return False
    return True

# define a function to calculate the minimun value in a piece
def calculate_min_value(value):
    x_min = min(value[i][0] for i in range(len(value)))
    y_min = min(value[i][1] for i in range(len(value)))
    for i in range(len(value)):
        value[i] = [value[i][0] - x_min, value[i][1] - y_min]
    return value

# list all shapes of pieces_1, the maximum number is 8
# use a set to save them since the points may occur in different order
def all_possibility(pieces_1):
    different_pieces = defaultdict(list)
    for key, value in pieces_1.items():
        value = calculate_min_value(value)
        for j in range(3):
            a = deepcopy(value)
            x_min = float('inf')
            y_min = float('inf')
            for i in range(len(a)):
                if j == 0:
                    a[i][0] = -a[i][0]
                if j == 1:
                    a[i][1] = -a[i][1]
                if j == 2:
                    a[i][0] = -a[i][0]
                    a[i][1] = -a[i][1]
                x_min = min(a[i][0], x_min)
                y_min = min(a[i][1], y_min)
            for i in range(len(a)):
                a[i] = [a[i][0] - x_min, a[i][1] - y_min]
            a = list(tuple(i) for i in a)
            different_pieces[key].append(set(a))
        different_pieces[key].append(set(tuple(i) for i in value))
    return different_pieces

# assess whether two pieces are identical
# if the pieces number in two files are different, return false
# if the one color in pieces_2 does not occur in pieces_1, return false
# if the points in pieces_2 are not the same points of the points of pieces_1, return false
def are_identical_sets_of_coloured_pieces(pieces_1, pieces_2):
    if not are_valid(pieces_1) or not are_valid(pieces_2):
        return False
    if len(pieces_1) != len(pieces_2):
        return False
    pieces1_part1 = all_possibility(pieces_1)
    for key, value in pieces_1.items():
        for i in range(len(value)):
            value[i][0], value[i][1] = value[i][1], value[i][0]
    pieces1_part2 = all_possibility(pieces_1)
    for key, value in pieces_1.items():
        for i in range(len(value)):
            value[i][0], value[i][1] = value[i][1], value[i][0]
    pieces_1_new = deepcopy(pieces1_part1)
    for key in pieces_1_new:
        pieces_1_new[key] = pieces1_part1[key] + pieces1_part2[key]
    for key, value in pieces_2.items():
        if key not in pieces_1_new:
            return False
        value = calculate_min_value(value)
        if set(tuple(i) for i in value) not in pieces_1_new[key]:
            return False
    return True

# calculate area of the pieces and the shape
def area_sum(graph):
    square = 0
    for colour, value in graph.items():
        points = value + [value[0]]
        square_a = 0
        square_b = 0
        for i in range(len(points) - 1):
            square_a += points[i][0] * points[i + 1][1]
            square_b += points[i][1] * points[i + 1][0]
        square += abs(square_a - square_b) / 2
    return square

# calculate equation in different edges, and calculate the how many times these equations occur
# at the same time, collect the middle points of every two points
def equation(tangram, dic):
    p = set()
    for key, value in tangram.items():
        points = value + [value[0]]
        for i in range(len(points) - 1):
            x1 = points[i]
            x2 = points[i + 1]
            if x1[1] == x2[1]:
                k = 'inf'
                b = x2[1]
                p.add(((x1[0] + x2[0])/2, x1[1]))
            elif x1[0] == x2[0]:
                k = 0
                b = x2[0]
                p.add((x1[0], (x1[1] + x2[1])/2))
            else:
                k = (x2[1] - x1[1])/(x2[0] - x1[0])
                b = (x1[1] * x2[0] - x2[1] * x1[0]) / (x2[0] - x1[0])
                xm = (x1[0] + x2[0])/2
                ym = (x1[1] * (x2[0] - xm) + x2[1] * (xm - x1[0])) / (x2[0] - x1[0])
                p.add((xm, ym))
            dic[k, b] += 1
    return p

# assess whether the point is on the edge of the shape
def is_on_edge(vertex, shape):
    for key, value in shape.items():
        points = value + [value[0]]
        for i in range(1, len(points)):
            s_x, e_x = min(points[i][0], points[i - 1][0]), max(points[i][0], points[i - 1][0])
            s_y, e_y = min(points[i][1], points[i - 1][1]), max(points[i][1], points[i - 1][1])
            if s_y == e_y and s_y == vertex[1]:
                if s_x <= vertex[0] <= e_x: # the vertex is on the parallel edge
                    return True
                else:
                    continue
            if s_x == e_x and s_x == vertex[0]:
                if s_y <= vertex[1] <= e_y: # the vertex is on the vertical edge
                    return True
                else:
                    continue
            if s_y == e_y:
                continue
            x = points[i][0] - (points[i][1] - vertex[1]) * \
                (points[i][0] - points[i - 1][0]) / (points[i][1] - points[i - 1][1])
            if x == vertex[0]:
                return True
    return False

# assess whether the point is in the shape
def is_in_shape(vertex, shape):
    intersect = 0
    for key, value in shape.items():
        points = value + [value[0]]
        for i in range(1, len(points)):
            s_x, e_x = min(points[i][0], points[i - 1][0]), max(points[i][0], points[i - 1][0])
            s_y, e_y = min(points[i][1], points[i - 1][1]), max(points[i][1], points[i - 1][1])
            if s_y == e_y: # the edge is parallel to the ray of the point
                continue
            elif s_y > vertex[1]:  # the edge is up to the point
                continue
            elif e_y < vertex[1]:  # the edge is down to the point
                continue
            elif e_x < vertex[0]:  # the edge is left to the point
                continue
            elif s_y == vertex[1]: # the lower endpoint of the edge is intersect with the vertex
                continue
            # elif e_y == vertex[1]: # the higher endpoint of the edge if  intersect with the vertex
            #     intersect += 1
            #     continue
            x = points[i][0] - (points[i][1] - vertex[1]) * \
                                (points[i][0] - points[i - 1][0]) / (points[i][1] - points[i - 1][1])
            if x < vertex[0]:
                continue
            intersect += 1
        if not intersect % 2:
            return False
    return True

# if the the number of every equation is small than 1, return false
# if the two shapes sum is different, return false
# if the middle points of every edge in tangram is not in shape, return false
def is_solution(tangram, shape):
    k_b = defaultdict(int)
    p = equation(tangram, k_b)
    equation(shape, k_b)
    for i in k_b:
        if k_b[i] <= 1:
            return False
    if area_sum(shape) != area_sum(tangram):
        return False
    for i in p:
        if not is_on_edge(i, shape):
            if not is_in_shape(i, shape):
                return False
    return True

