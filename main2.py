# Heliene USA Solar Panel Edge Measurement Utility

# Authors:

# Jaquelyn E Hyde
# jaquelyn.hyde@ire.minnstate.edu

# Elvis Enang

# Hannah Adeyemi

# Luhana Zorrilla

from pathlib import Path

import numpy as np
import cv2 as cv

# TODO: implement a better way to grab the image. OpenCV has UI controls.
root_dir = Path(__file__).resolve().parent
inputfilename = root_dir / "Test_Image.jpg"
outputfilename = root_dir / "Output.jpg"

# Given:    Two 2D points
# Return:   The euclidean distance between them
def calculate_distance(pt1, pt2):
    return np.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

# Given:    An image
# Return:   A UI that lets the user click and calculate distances
def manual_inspection():
    return 0
    # crickets
    # this can be mostly copied from the earlier version but there are some important modifications

# Given:    An image
# Return:   An edge-detected image
def detect_edges(image):
    # Apply Canny edge detection
    edges = cv.Canny(image, 100, 200)

    return edges

# Given:    An edge-detected image
# Return:   A list of contours in that image
def index_contours(image):
    return 0
    # crickets

# Given:    A set of contours
# Return:   A list of horizontal/vertical vectors connecting them
def gauge_contours():
    return 0
    # crickets

# Given:    An image
# Return:   An image with each distinct area labeled
#           In the long term this should 'find' the backsheet/overhang by feature recognition
def index_areas(image):
    return 0
    # crickets

# Given:    An image with a calibration target
#           The length in mm of a square in the target
# Return:   The pixel-to-mm ratio of the plane of the calibration target
def calibrate_image(image, length):
    return 0
    # crickets

# Given:    An image
# Return:   The matrix that describes distortion in the image
#           (i need more help understanding this part...)
def calibrate_distortion(image):
    return 0
    # crickets

# Given:    An image of a solar panel
# Perform:  The inspection routine as requested by Heliene:
#               Find all edges in the image
#               Label all edges in the image
#               Measure distances between the backsheet and laminate protrustion
#               Return good/not good status
def inspect_panel():
    return 0
    # crickets

# Given:    The requested information (clarify w/ danver)
# Return:   A JSON callback providing it, GOOD/NOT GOOD status
def json_callback():
    return 0
    # crickets

# Access a given connected camera
# A certain keypress should take a snapshot and initiate the edge characterization routine
# I am not sure if this needs to be a seperate function? We'll see how development goes
def camera_controller():
    return 0
    # crickets

# Provide a convenient interface to use the utility
def user_interface():
    return 0
    # crickets

# TODO: add an option to capture a single image and keep it
# i.e. keep capturing live video frames, but only use the last chosen one for edge detection

def debug_user_interface():
    # draw a ui with three panels

    wait_time = 25
    height = 1280
    width = 1920 # change to grab user resolution? these are just from my monitor -j

    ui_image = np.zeros((height, width, 3), np.uint8)

    panel_height = height // 4
    panel_width = width // 4

    # TODO: add bit that runs the camera controller...

    cv.namedWindow('EMU - Debug')

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print('Unable to open camera')
        exit()

    while(1):
        ret, frame = cap.read()

        if not ret:
            print('Unable to read frame')
            break

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        edges = detect_edges(gray)

        # its unclear if this needs to happen this way and how it affects performance
        r_frame = cv.resize(frame, (panel_width, panel_height))
        r_gray = cv.cvtColor(cv.resize(gray, (panel_width, panel_height)),cv.COLOR_GRAY2BGR)
        r_edges = cv.cvtColor(cv.resize(edges, (panel_width, panel_height)),cv.COLOR_GRAY2BGR)

        ui_image[10:10+panel_height, 10:10+panel_width] = r_frame
        ui_image[10+panel_height:10+2*panel_height, 10:10+panel_width] = r_gray
        ui_image[10+panel_height:10+2*panel_height, 10+panel_width:10+2*panel_width] = r_edges

        cv.imshow('EMU - Debug', ui_image)

        if cv.waitKey(wait_time) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()

# Initiate a loop:
#       Wait for user input:
#           If (A) - Use test image, go to ()
#           If (B) - Connect to camera, wait for user input:
#               If (C) - Take image, go to ()
#               If (D) - Exit camera loop (should be able to do this from (C) too
#           (C) - Show image and edge enhanced image, list of contours, regions
#                 Automatically or manually measure between designated contours
#                 Display side by side or overlaid: original image, edge enhanced image, area labeled, etc

# Used for testing purposes. If you run main.py directly, it will do this
# TODO: We should change the main file name to something more descriptive
# TODO: We really need to change the functions to take images and not paths...
# TODO: This could initiate a more useful debugging loop (see pseudocode in paragraph above)
def main():
    image = cv.imread(inputfilename)
    edge_image = detect_edges(image)
    cv.imwrite("Output.jpg", edge_image)

    debug_user_interface()


if __name__ == "__main__":
    main()
