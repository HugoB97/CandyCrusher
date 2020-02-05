from itertools import groupby
import pandas as pd
import cv2
import pprint

colour_dict = {"Y": "Yellow",
               "R": "Red",
               "B": "Blue",
               "G": "Green",
               "O": "Orange",
               "P": "Purple"}

lst = [['Y', 'P', 'O', 'G', 'O', 'R', 'R', 'O'],
       ['B', 'Y', 'R', 'P', 'B', 'B', 'O', 'P'],
       ['Y', 'Y', 'R', 'G', 'P', 'B', 'G', 'Y'],
       ['P', 'R', 'O', 'B', 'B', 'R', 'Y', 'R'],
       ['G', 'G', 'Y', 'Y', 'R', 'R', 'G', 'R']]

coords = []

df = pd.DataFrame(lst)
move_dict = {}
go_cnt = 0


def disp(image):
    image = cv2.imread("ImageFolder/" + image)
    cv2.imshow("Your Level", image)
    cv2.waitKey(0)
    return 0


def decision(image):
    print("\nThere are", go_cnt, "possible moves\n")
    for x in range(1, go_cnt + 1):
        print("Move number", x, "moves the candy at position", move_dict[x][1], move_dict[x][2],
              "for a crush with", move_dict[x][3], colour_dict[move_dict[x][0]], "candy")
    # image = cv2.imread("ImageFolder/" + image)
    cv2.imshow("Your Level", image)
    print("\nWhich move would you like to complete? ")
    move_chosen = cv2.waitKey(0) - 48
    cv2.destroyAllWindows()
    if move_chosen not in range(1, go_cnt + 1):
        print("invalid move: Move 1 selected")
        move_chosen = 1
    else:
        print("You Chose Move", move_chosen)
    return move_dict[int(move_chosen)]


def move_tracking(pos, direct, colour, candy):
    mt_list = [colour, pos, direct, candy]
    move_dict[go_cnt] = mt_list


def match_check(edited_df, pos, direction):
    global go_cnt
    df_copy = edited_df.copy()

    # Create a transpose of the df to turn rows into columns, one function to iterate both rows and cols
    trans = df_copy.transpose()
    dfs = [df_copy, trans]
    for df in dfs:
        for x in df:
            # Access each column in list format
            col = list(df[x])
            # Matches of 3, 4, 5
            for num in range(3, 6):
                for k, g in groupby(col):
                    match_col = list(g)
                    if len(match_col) == num:
                        color = match_col[0]
                        match_num = len(match_col)
                        go_cnt += 1
                        move_tracking(pos, direction, color, match_num)


def move_down(md_pos, md_df):
    df_copy = md_df.copy()  # Use copy function as direct assignment creates two instances of the same DF
    r, c = md_pos
    a = df_copy.loc[r, c]
    b = df_copy.loc[r + 1, c]
    df_copy.loc[r, c] = b
    df_copy.loc[r + 1, c] = a
    match_check(df_copy, md_pos, "Down")


def move_right(mr_pos, mr_df):
    df_copy = mr_df.copy()
    r, c = mr_pos
    a = df_copy.loc[r, c]
    b = df_copy.loc[r, c + 1]
    df_copy.loc[r, c] = b
    df_copy.loc[r, c + 1] = a
    match_check(df_copy, mr_pos, "Right")


def move(move_df, image):
    h, w = move_df.shape
    r = h - 1
    c = w - 1
    for row in range(0, h):
        for col in range(0, w):
            current_pos = (row, col)
            if col == c and row != r:
                move_down(current_pos, move_df)
            if col != c and row == r:
                move_right(current_pos, move_df)
            if col != c and row != r:
                move_down(current_pos, move_df)
                move_right(current_pos, move_df)

    moves = decision(image)
    return moves
