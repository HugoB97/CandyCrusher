import cv2


def view_image(image):
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def arrow(image, move, arr):
    # move = dic[1]
    # image = cv2.imread("ImageFolder/" + image)
    pos_x = move[1][0]
    pos_y = move[1][1]
    dir = move[2]
    end_point = 0
    arr_pos = arr[pos_x][pos_y]
    if dir == 'Right':
        pos_y = pos_y + 1
        end_point = tuple(arr[pos_x][pos_y])
    elif dir == 'Down':
        pos_x = pos_x + 1
        end_point = tuple(arr[pos_x][pos_y])
    colour = (0, 0, 0)
    start_point = tuple(arr_pos)
    arrow = cv2.arrowedLine(image, start_point, end_point, colour, thickness=4)
    cv2.imwrite('ArrowImage.png', arrow)
    cv2.imshow("image", arrow)
    cv2.waitKey(0)
