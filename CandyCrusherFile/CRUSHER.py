import easygui as ui
import cv2
import os
import twoSweetLocation
import oneSweetSeperation
import threeMoveGeneration
import arrow

"""
The 'CandyCrusherUI.py' file creates the user interface that the user will see.
A message box with a welcome message is created using the easygui 'ui.msgbox()' function, next the user will be asked to
select an image of a level that they are stuck on. This is done using the easygui 'ui.fileopenbox()' function. This image
is then passed to the 'othercode()' function which displays the level that the user selected and gives them 2 options:
- "Auto-Complete" will call the 'sweet_separation()', 'sweet_location()', 'threeMoveGeneration.move()' and 'arrow()'
functions.
- "EXIT" will close the application
This is done using the easygui 'ui.buttonbox()' function.
"""


def start_the_fun(sf_image, sf_choice):
    finish = "Start"
    while finish == "Start":
        if finish == "Quit":
            break
        choices = ["Auto-Complete", "EXIT"]
        reply = ui.buttonbox("Click 'Auto-Complete' to list all available moves: "
                             "\n\nClick 'EXIT' to close application:", image=sf_choice, choices=choices)
        if reply == "Auto-Complete":
            oneSweetSeperation.sweet_separation(sf_image)
            sweets_located, coords = twoSweetLocation.sweet_location(sf_image)
            move_dict = threeMoveGeneration.move(sweets_located, sf_image)
            arrow.arrow(sf_image, move_dict, coords)
            os.remove("ArrowImage.png")
            exit()
        elif reply == "EXIT":
            exit()


ui.msgbox("Welcome to the Candy Crusher!!! Please choose the level you are stuck on:")
choice = ui.fileopenbox()
image = cv2.imread(choice)
start_the_fun(image, choice)
