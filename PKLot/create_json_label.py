"""
Simple script for preprosessing PKLot label data (.xml)
"""

import os
import json
import glob
import xmltodict
import PKLot.config
import PKLot.utilities


def get_label_data(xml_path):

    with open(xml_path) as xml:
        xml_dict = xmltodict.parse(xml.read())

    return xml_dict


def get_PKLot_label_json(parking_lots_data, save_path, root_filename):

    classes = {"0": "Not-Car", "1": "Car"}

    annotations = []

    for parking_lot_data in parking_lots_data["parking"]["space"]:

        if "@occupied" in parking_lot_data:

            x, y, width, height = PKLot.utilities.get_bouding_box(parking_lot_data["contour"]["point"])
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

    data_dir = PKLot.config.preprocess_config["data_dir"]

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