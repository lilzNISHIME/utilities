import os
import json
import glob
import xmltodict
import itertools
import config


def get_label_data(xml_path):

    with open(xml_path) as xml:
        xml_dict = xmltodict.parse(xml.read())

    return xml_dict


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


def get_PKLot_label_json(parking_lots_data, save_path, root_filename):

    classes = {"0": "Not-Car", "1": "Car"}

    annotations = []

    for parking_lot_data in parking_lots_data["parking"]["space"]:

        if "@occupied" in parking_lot_data:

            x, y, width, height = get_bouding_box(parking_lot_data["contour"]["point"])
            annotation = {
                "class": classes[parking_lot_data["@occupied"]],
                "height": height,
                "type": "rect",
                "width": width,
                "x": x,
                "y": y
            }

            annotations.append(annotation)

    data_dict = {
        "annotations": annotations,
        "class": "image",
        "filename": os.path.join(save_path, root_filename + ".jpg")
    }

    return json.dumps(data_dict, sort_keys=True, indent=2)


def main():

    data_dir = config.preprocess_config["data_dir"]

    label_data_path = os.path.join(data_dir, "label", "*.xml")
    # data_path = os.path.join(data_dir, "data")

    output_dir = os.path.join(data_dir, "format")
    output_label_dir = os.path.join(output_dir, "label_json")
    # output_data_dir = os.path.join(output_dir, "data")

    label_paths = glob.glob(label_data_path)

    for path in label_paths:

        parking_lots_data = get_label_data(path)
        save_path = os.path.dirname(path)
        root_filename = os.path.splitext(os.path.basename(path))[0]

        label_json = get_PKLot_label_json(parking_lots_data, save_path, root_filename)

        if not os.path.exists(output_dir):

            os.mkdir(output_dir)

        if not os.path.exists(output_label_dir):

            os.mkdir(output_label_dir)

        output_path = os.path.join(output_label_dir, root_filename + ".json")

        with open(output_path, "w") as file:

            file.write(label_json)


if __name__ == "__main__":
    main()