"""
Module with various utilities for PKLot dataset
"""

import itertools


def get_bouding_box(coordinates):
    """
    Given polygonal coordinates, compute coordinates of rectangle surround it
    :param coordinates: list of coordinates representing bounding box
    :return: left top coordinate, width and height
    """

    all_coordinate = get_all_intersection(coordinates)

    left_top = get_left_top_coordinate(all_coordinate)
    right_down = get_right_down_coordinate(all_coordinate)

    width = right_down[0] - left_top[0]
    height = right_down[1] - left_top[1]

    return left_top[0], left_top[1], width, height


def get_left_top_coordinate(coordinates):
    """
    Given coordinates, return left top coordinate
    :param coordinates: list of lists representing x and y coordinates
    :return: left top coordinate
    """

    min_x = min(coordinates, key=lambda c: c[0])[0]
    left_coordinates = [p for p in coordinates if p[0] == min_x]

    if len(left_coordinates) == 1:
        return left_coordinates[0]

    else:
        return min(left_coordinates, key=lambda c: c[1])


def get_right_down_coordinate(coordinates):
    """
    Given coordinates, return right down coordinate
    :param coordinates: list of lists representing x and y coordinates
    :return: right down coordinate
    """

    max_x = max(coordinates, key=lambda c: c[0])[0]
    right_coordinates = [p for p in coordinates if p[0] == max_x]

    if len(right_coordinates) == 1:
        return right_coordinates[0]

    else:
        return max(right_coordinates, key=lambda c: c[1])


def get_all_intersection(coordinates):
    """
    Given coordinates, compute coordinates of bounding boxes.
    :param coordinates: list of lists representing x and y coordinate
    :return: list of lists representing x and y coordinates
    """

    coordinates_list = [list(map(int, p.values())) for p in coordinates]
    all_coordinates = []

    for points in list(itertools.combinations(coordinates_list, 2)):

        all_coordinates.extend(get_bouding_box_coordinate(*points))

    all_coordinates.extend(coordinates_list)

    return all_coordinates


def get_bouding_box_coordinate(first, second):

    return [first[0], second[1]], [second[0], first[1]]
