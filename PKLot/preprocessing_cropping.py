"""
Simple script for preprocessing PKLot dataset.
convert xml label data to json and cropping image.
"""

import cv2
import glob
import json
import os
import tqdm

import PKLot.config
import PKLot.utilities


def load_image(path):

    return cv2.imread(path)


def marge_all_cordinates(label_path):

    all_parking_lot_coordinate = []

    for single_parking_lot_data in label_path["parking"]["space"]:

        if "@occupied" in single_parking_lot_data:

            coordinates = [list(map(int, c.values())) for c in single_parking_lot_data["contour"]["point"]]
            all_parking_lot_coordinate.extend(coordinates)

    return all_parking_lot_coordinate


def get_minimum_bounding_box(label_path):

    all_parking_lot_coordinate = marge_all_cordinates(label_path)

    return PKLot.utilities.get_bounding_box(all_parking_lot_coordinate)


def get_PKLot_label_json_with_fit_coordinate(parking_lots_data, save_path, root_filename, init_x, init_y):

    classes = {"0": "Not-Car", "1": "Car"}

    annotations = []

    for parking_lot_data in parking_lots_data["parking"]["space"]:

        if "@occupied" in parking_lot_data:

            coordinates_list = [list(map(int, p.values())) for p in parking_lot_data["contour"]["point"]]
            x, y, width, height = PKLot.utilities.get_bounding_box(coordinates_list)
            annotation = {
                "class": classes[parking_lot_data["@occupied"]],
                "height": height,
                "type": "rect",
                "width": width,
                "x": x - init_x,
                "y": y - init_y
            }

            annotations.append(annotation)

    data_dict = {
        "annotations": annotations,
        "class": "image",
        "filename": os.path.join(save_path, root_filename + ".jpg")
    }

    return json.dumps(data_dict, sort_keys=True, indent=2)


def data_cleansing(dataset_dir):

    label_path = glob.glob(os.path.join(dataset_dir, "label", "*.xml"))
    data_paths = os.path.join(dataset_dir, "data")

    output_dir = os.path.join(dataset_dir, "cropped")
    output_label_dir = os.path.join(output_dir, "label")
    output_data_dir = os.path.join(output_dir, "data")

    if not os.path.exists(output_dir):

        os.mkdir(output_dir)

    if not os.path.exists(output_label_dir):

        os.mkdir(output_label_dir)

    if not os.path.exists(output_data_dir):

        os.mkdir(output_data_dir)

    for path in label_path:

        parking_lots_data = PKLot.utilities.get_label_data(path)
        filename = os.path.splitext(os.path.basename(path))[0]
        save_path = os.path.dirname(path)

        image = load_image(os.path.join(data_paths, filename + ".jpg"))

        x, y, width, height = get_minimum_bounding_box(parking_lots_data)
        cropped_image = image[y:y+height, x:x+width]

        output_image_path = os.path.join(output_data_dir, filename + ".jpg")
        cv2.imwrite(output_image_path, cropped_image)

        cropped_label_json = get_PKLot_label_json_with_fit_coordinate(parking_lots_data, save_path, filename, x, y)
        output_label_path = os.path.join(output_label_dir, filename + ".json")

        with open(output_label_path, "w") as file:

            file.write(cropped_label_json)


def main():

    dataset_dirs = PKLot.config.preprocess_config["data_dir"]

    for dataset_dir in tqdm.tqdm(glob.glob(dataset_dirs)):

        data_cleansing(dataset_dir)



if __name__ == "__main__":
    main()