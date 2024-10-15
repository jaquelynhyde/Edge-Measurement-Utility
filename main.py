# Heliene USA Solar Panel Edge Measurement Utility

# Authors:

# Jaquelyn E Hyde
# jaquelyn.hyde@ire.minnstate.edu

# Elvis Enang

# Hannah Adeyemi

# Luhana Zorrilla
# Luhana.zorrilla@ire.minnstate.edu

from pathlib import Path

import numpy as np
import cv2

# TODO: implement a better way to grab the image. OpenCV has UI controls.
root_dir = Path(__file__).resolve().parent
inputfilename = root_dir / "Test_Image.jpg"
outputfilename = root_dir / "Output.jpg"

def calculate_distance(pt1, pt2):
    return np.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

# Return the distance between two points on an image, input with the mouse
# TODO: we need a version of this that works automatically in the long term
def measure_distance(image_path):

    image = cv2.imread(image_path)

    points = []

    # Function to handle mouse clicks for distance measurement
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Image", image)

            if len(points) == 2:
                # Calculate the distance between the two points in pixels
                pixel_distance = calculate_distance(points[0], points[1])

                print("Calculated distance: " + str(pixel_distance) + " pixels")

                # Draw a line between the points
                cv2.line(image, points[0], points[1], (255, 0, 0), 2)
                cv2.imshow("Image", image)

    # Display the image and set up the mouse callback
    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", mouse_callback)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Return an image processed with Canny edge detection
def detect_edges(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 100, 200)

    return edges

# Used for testing purposes. If you run main.py directly, it will do this
# TODO: We should change the main file name to something more descriptive
# TODO: We really need to change the functions to take images and not paths...
def main():
    edge_image = detect_edges(inputfilename)
    cv2.imwrite("Output.jpg", edge_image)
    measure_distance(outputfilename)

if __name__ == "__main__":
    main()

