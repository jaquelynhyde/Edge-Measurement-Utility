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
    # crickets
    # this can be mostly copied from the earlier version but there are some important modifications

# Return an image processed with Canny edge detection
# TODO: change to work with an image, instead of reading the image itself
def detect_edges(image_path):
    # Read the image
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv.Canny(image, 100, 200)

    return edges

# Given:    An edge-detected image
# Return:   A list of contours in that image
def index_contours(image):
    # crickets

# Given:    A set of contours
# Return:   A list of horizontal/vertical vectors connecting them
def gauge_contours():
    # crickets

# Given:    An image
# Return:   An image with each distinct area labeled
#           In the long term this should 'find' the backsheet/overhang by feature recognition
def index_areas(image):
    # crickets

# Given:    An image with a calibration target
# Return:   The pixel-to-mm ratio of the plane of the calibration target
def calibrate_image(image):
    # crickets

# Given:    An image
# Return:   The matrix that describes distortion in the image
#           (i need more help understanding this part...)
def calibrate_distortion(image):
    # crickets

# Given:    An image of a solar panel
# Perform:  The inspection routine as requested by Heliene:
#               Find all edges in the image
#               Label all edges in the image
#               Measure distances between the backsheet and laminate protrustion
#               Return good/not good status
def inspect_panel():
    # crickets

# Given:    The requested information (clarify w/ danver)
# Return:   A JSON callback providing it, GOOD/NOT GOOD status
def json_callback():
    # crickets

# Access a given connected camera
# A certain keypress should take a snapshot and initiate the edge characterization routine
# ***it is very important that you release the camera when you're done using it: read the tutorials***
def camera_controller():
    # crickets

# Provide a convenient interface to use the utility
def user_interface():
    # crickets

# Provide a convenient interface *for us* to use and debug the utility
# See the description above main() for more info on what this could do and subroutines to make
def debug_user_interface():
    # crickets
    
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
    edge_image = detect_edges(inputfilename)
    cv2.imwrite("Output.jpg", edge_image)

if __name__ == "__main__":
    main()
