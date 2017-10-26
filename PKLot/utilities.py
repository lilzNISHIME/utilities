"""
Module with various utilities for PKLot dataset
"""

import xmltodict


def get_bounding_box(coordinates):
    """
    Given polygonal coordinates, compute coordinates of rectangle surround it
    :param coordinates: list of coordinates representing bounding box
    :return: left top coordinate, width and height
    """

    top = min(coordinates, key=lambda c: c[1])[1]
    bottom = max(coordinates, key=lambda c: c[1])[1]
    left = min(coordinates, key=lambda c: c[0])[0]
    right = max(coordinates, key=lambda c: c[0])[0]

    width = right - left
    height = bottom - top

    return left, top, width, height


def get_label_data(xml_path):

    with open(xml_path) as xml:
        xml_dict = xmltodict.parse(xml.read())

    return xml_dict
