import os.path
import numpy as np
import cv2
import json
import config


def main():

    path = config.preprocess_config["visualize_data"]

    target_json = os.path.join(path, "label/2012-09-12_06_05_16.json")
    target_img = os.path.join(path, "data/2012-09-12_06_05_16.jpg")

    image = cv2.imread(target_img)

    with open(target_json) as file:

        labels = json.load(file)

    all_contour = []
    for label in labels["annotations"]:

        if label["class"]:

            contour = [
                [label["x"], label["y"]],
                [label["x"]+label["width"], label["y"]],
                [label["x"]+label["width"], label["y"]+label["height"]],
                [label["x"], label["y"]+label["height"]]
                ]
            all_contour.append(contour)

    for points in all_contour:

        plotting_points = [np.array(points).reshape((-1,1,2))]
        image = cv2.polylines(image, plotting_points, True, (0, 255, 255))

    cv2.imwrite("sample_cropped.jpg", image)


if __name__ == "__main__":
    main()

