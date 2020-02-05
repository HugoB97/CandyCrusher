import cv2
import os
import shutil
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def color_frame(list, rows_cnt, image):
    color_list = []
    final_list = []
    # image = cv2.imread("ImageFolder/" + image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # plt.imshow(image)
    # plt.show()
    debug = []
    for x in list:
        for y in x:

            color_value = image[y[1], y[0]]
            color_value = color_value.tolist()
            debug.append(color_value)
            if color_value[0] in range(240, 256):
                if color_value[2] in range(0, 40):
                    if color_value[1] in range(0, 10):
                        color = "R"
                        color_list.append(color)
                    elif color_value[1] in range(220, 245):
                        color = "Y"
                        color_list.append(color)
                    elif color_value[1] in range(125, 155):
                        color = "O"
                        color_list.append(color)
            elif color_value[2] in range(240, 256):
                if color_value[1] in range(140, 170) and color_value[0] in range(20, 50):
                    color = "B"
                    color_list.append(color)
                elif color_value[1] in range(25, 70) and color_value[0] in range(195, 230):
                    color = "P"
                    color_list.append(color)
            elif color_value[0] in range(40, 75) and color_value[1] in range(170, 210) and color_value[2] in range(0,
                                                                                                                   15):
                color = "G"
                color_list.append(color)

            else:
                color_list.append("X")
                print("Error", color_value)
    color_list = np.array_split(np.array(color_list), rows_cnt)
    for x in color_list:
        x = x.tolist()
        final_list.append(x)
    return final_list


def sort(sub_li):
    sub_li.sort(key=lambda x: x[0])
    return sub_li


def sweet_location(image):
    main_list, reverse, y_vals, y_nested, y_dict, objects, ints_here = [], [], [], [], [], [], []
    cnt = 0

    # Code Checks to ensure image exists in the correct directory
    folder = Path("ImageFolder")
    if not os.path.exists(folder):
        print("Path to Image Does not Exist, Path Created: Please Run code again")
        os.mkdir(folder)
        if not os.path.isfile("Final.jpg"):
            print("'Final.jpg' does not exist, please add to project")
            exit()
        shutil.move("Final.jpg", "ImageFolder/Final.jpg")
        exit()

    # Open filter the image in GrayScale
    imgpth = "ImageFolder" + "/" + "Final.jpg"
    im = cv2.imread(imgpth, cv2.IMREAD_GRAYSCALE)

    # Set Threshold to 255 to turn sweets black and background completely white
    _, binary = cv2.threshold(im, thresh=225,
                              maxval=255,
                              type=cv2.THRESH_BINARY)

    # Create a Shape and apply Opening Filter on the image
    shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opening_image = cv2.morphologyEx(binary, cv2.MORPH_OPEN, shape)

    # Setup params for blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 15
    params.filterByColor = True
    params.blobColor = 0
    params.filterByCircularity = True
    params.minCircularity = 0.1
    params.filterByConvexity = True
    params.minConvexity = 0.87
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(opening_image)

    # Sort blob locations into a nested list
    for k in keypoints:
        tuple2int = []
        for n in k.pt:
            tuple2int.append(int(n))
        ints_here.append(list(tuple2int))
        objects.append((int(k.pt[0] - k.size), int(k.pt[1] - k.size), int(k.size * 2), int(k.size * 2)))
    # Display below code to check where blobs are detected
    im_with_keypoints = cv2.drawKeypoints(opening_image, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # plt.imshow(im_with_keypoints, cmap="gray")
    # plt.show()
    # cv2.imshow("Blobs", im_with_keypoints)
    # cv2.imwrite("blobs.jpg", im_with_keypoints)
    # cv2.waitKey(0)

    # Reverse Order
    for x in reversed(ints_here):
        reverse.append(x)

    # Get Y values
    for x in reverse:
        y_vals.append(x[1])

    # Create a dictionary with values grouped
    for k, g in itertools.groupby(y_vals, key=lambda n: n // 10):
        # y_dict[cnt] = list(g)
        y_nested.append(list(g))
        cnt += 1

    col_count = len(y_nested[0])
    row_cnt = len(reverse) / col_count
    split_np_array = np.split(np.array(reverse), row_cnt)

    for x in split_np_array:
        x = x.tolist()
        tt = sort(x)
        main_list.append(tt)

    coord_df = pd.DataFrame(main_list)
    final = color_frame(main_list, row_cnt, image)
    color_df = pd.DataFrame(final)
    os.remove("ImageFolder/Final.jpg")

    return color_df, main_list

