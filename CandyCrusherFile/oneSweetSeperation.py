import cv2
import os
from pathlib import Path
import numpy as np
from PIL import Image

"""
The "oneSweetSeparation.py" file is in charge of separating each type of sweet so they can be located later and put into
a grid so that potential moves can be analysed.
This file contains 7 functions, there is 1 main function "sweet_separation" that calls the other 6 minor functions.
The main function "sweet_separation" only takes 1 input: the image of the level that the user is stuck on, and operates
as follows:
- Checks that the image exists in the right directory using the 'os.path.exists()' function and prints out an error
message if the image does not.
- Then separates each of the 6 sweet types out individually using either the 'yuv_separator()'[orange and yellow sweets]
or 'rgb_separator()'[green, blue, purple and red sweets] functions which both take 3 inputs: the image, a lower RGB/YUV
threshold array and an upper RGB/YUV threshold array. Both of these functions use the lower and upper thresholds to
create a mask for the particular sweet. A for-if loop is then used to check each pixel in the original image. If the
pixel is within the range then it is untouched, if the pixel is outside of the range it is changed to white. What is
returned is just the requested sweet with a white background.
- Each image of the isolated sweets is then passed into the 'blur()' function, this function blurs the image using the
'cv2.filter2D()' function in conjunction with a blurring kernel.
- Each image is then sharpened using the 'sharpen()' function, this function sharpens the image using the 'cv2.filter2D()'
 function in conjunction with a sharpening kernel.
- Each image is then passed to the 'transparent()' function which converts the image to a RGBA image using the
'img.convert("RGBA")' function. A for-if loop then checks for every white pixel and changes its 'A' value to 0, this
creates an image of just the desired sweet with a transparent background.
- All these images are then combined using the 'combine()' function. This functions combines 2 images together using the
'background.paste()' function.
The end result 'Final.jpg' is all the sweets within specific ranges and a transparent background. This image is then used
for sweet location.
"""

# Function that displays the image
def view_image(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def sharpen(img):
    # generating the kernels
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    output = cv2.filter2D(img, -1, kernel)
    return output


def blur(image):
    kernel = np.array([[(1 / 9), (1 / 9), (1 / 9)], [(1 / 9), (1 / 9), (1 / 9)], [(1 / 9), (1 / 9), (1 / 9)]])
    output = cv2.filter2D(image, -1, kernel)
    return output


def rgb_separator(image, low_range, high_range):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    original = rgb.copy()
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mask_red = cv2.inRange(rgb, low_range, high_range)
    rows, cols, layers = image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            k = mask_red[i, j]
            if k < 200:
                original[i, j] = [255, 255, 255]
    sweets = original
    return sweets


def yuv_separator(image, low_range, high_range):
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    original = rgb.copy()
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    mask_red = cv2.inRange(yuv, low_range, high_range)
    rows, cols, layers = image.shape
    for i in range(0, rows):
        for j in range(0, cols):
            k = mask_red[i, j]
            if k < 200:
                original[i, j] = [255, 255, 255]
    sweets = original
    return sweets


def transparent(image, name):
    cv2.imwrite(name, image)
    img = Image.open(name)
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    img.putdata(new_data)
    img.save(name, "PNG")


def combine(image1, image2, name):
    background = Image.open(image1)
    foreground = Image.open(image2)
    background.paste(foreground, (0, 0), foreground)
    background.save(name, "PNG")


def sweet_separation(image):
    # Code Checks to ensure image exists in the correct directory
    folder = Path("ImageFolder")
    if not os.path.exists(folder):
        print("Path to Image Does not Exist, Path Created: Please add images to the Image Folder")
        os.mkdir(folder)
        exit()

    # image = cv2.imread("ImageFolder" + "/" + img_name)

    # Orange Sweets
    orange_sweets = yuv_separator(image, np.array([85, 50, 195]), np.array([180, 100, 235]))
    orange_sweets = sharpen(orange_sweets)
    transparent(orange_sweets, "OrangeSweets.png")

    # Yellow Sweets
    yellow_sweets = yuv_separator(image, np.array([120, 20, 160]), np.array([215, 70, 190]))
    yellow_sweets = sharpen(yellow_sweets)
    transparent(yellow_sweets, "YellowSweets.png")

    # Purple Sweets
    purple_sweets = rgb_separator(image, np.array([150, 25, 160]), np.array([225, 70, 255]))
    purple_sweets = sharpen(purple_sweets)
    transparent(purple_sweets, "PurpleSweets.png")

    # Blue Sweets
    blue_sweets = rgb_separator(image, np.array([10, 80, 170]), np.array([60, 160, 255]))
    blue_sweets = sharpen(blue_sweets)
    transparent(blue_sweets, "BlueSweets.png")

    # Red Sweets
    red_sweets = rgb_separator(image, np.array([110, 0, 0]), np.array([255, 30, 20]))
    red_sweets = sharpen(red_sweets)
    transparent(red_sweets, "RedSweets.png")

    # Green Sweets
    green_sweets = rgb_separator(image, np.array([20, 85, 0]), np.array([75, 255, 20]))
    green_sweets = sharpen(green_sweets)
    transparent(green_sweets, "GreenSweets.png")

    # Combining the sweets
    combine("OrangeSweets.png", "YellowSweets.png", "BG1.png")  # Combining Orange & Yellow
    combine("PurpleSweets.png", "BlueSweets.png", "BG2.png")  # Combining Purple & Blue
    combine("RedSweets.png", "GreenSweets.png", "BG3.png")  # Combining Red & Green
    combine("BG1.png", "BG2.png", "BG4.png")  # Combining Orange & Yellow & Purple & Blue
    combine("BG3.png", "BG4.png", "Final.png")  # Combining Orange & Yellow & Purple & Blue & Red & Green

    final = cv2.imread("Final.png")
    final = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
    cv2.imwrite("ImageFolder" + "/" + "Final.jpg", final)

    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith('.png'):
            os.remove(file)
