# Edge Measurement Utility

Created by Team Heliene USA as part of the IRE Fall 2024 Industry Design Project\

-Elvis Enang
-Hannah Adeyemi
-Luhana Zorrilla
-Jaquelyn E Hyde

# How to Use This Software (Standalone)
1. Ensure your device is connected to a camera
2. Print out the default 'checkerboard' target from https://calib.io/pages/camera-calibration-pattern-generator
3. Lay the checkerboard target next to and on the same surface of whatever you are detecting the edges of
4. Orient your camera so that the lens is parallel with the calibration target, and keep your camera at this distance from the target during operation
5. Run EdgeMeasurementUtility.py
6. A live feed will open and display detected eges
7. Press 'm' to toggle measurement mode on and off. With measurement mode on, you can select two edges in the image, highlighted in green, and produce measurements between them which will be reported on screen.
8. When you are done, ensure measurement mode is off, and press escape or close the window.

# Description

The Edge Measurement Utility (EMU) is a class-based implementation of the OpenCV library built to take an input image, find contours within it, and allow the user to locate contours at x/y points in the image, automatically measuring between them and reporting the minimum and maximum horizontal and vertical distances. 

The Edge Measurement Utility may be ran as standalone software, in which case it will open a window and a connected camera, creating a live feed of images from which snapshots may be taken for edge measurement. By changing the self.use_uploaded_image flag, it can instead use an image named in self.loaded_image

For the current standalone user interface, EMU assumes that your initial image on startup contains a checkerboard calibration target like the default checkerboard target generated here: 

https://calib.io/pages/camera-calibration-pattern-generator

All further images should be taken with the orientation of the camera and the imaged surface remaining the same

i.e. the camera should be oriented so the camera lens and the solar panel are parallel, with a printed calibration target visible in the first image, layed on the same surface and at the same level as the panel. All further images should be taken with the camera only moving left/right relative to the panel, not up/down.

EMU is also usable as an object within other software. However, some changes to code may be necessary. Reccomendations for future work are detailed in 'Variable and Function Descriptions'

# Variable and Function Descriptions

## __init__(self):
Initializes the edge measurement utility
Sets the mm_pixel_ratio to 1 by default

## horizontal_distance(point1, point2)
Returns the absolute value of point1[0] - point2[0]

## vertical_distance(point1, point2)
Returns the absolute value of point1[1] - point2[1]

## calibrate_mm_to_pixel_ratio(image, rows, cols, square_mm)
Given an image with a checkerboard calibration target in it, the number of rows and columns in the calibration target, and the length of the side of an individual square on the board, returns the ratio of millimeters per pixel in the image

Currently, this is implemented as a static method and returns a value. To improve functionality and compatability with other software using EMU as a class, this should probably be changed to directly set self.mm_pixel_ratio

Returns -1 if no calibration target was found in the image

## detect_edges(image, min_val, max_val):
Given an image and a minimum and maximum value, returns an edge detected image (a black and white image with edges in white)

The minimum and maximum value are used for Canny edge detection. Canny edge detection measures changes in image intensity at every point in the image. The minimum value is the threshhold below which nothing will be considered an edge, the maximum value (reccomended to be 3 times min val) is the threshhold above which everything is an edge, and between the two Canny edge detection does additional checks to determine if it is an edge

## feature_detection():
Does nothing at this moment - is a stand in for future feature detection methods

## select_contour(self, x, y): 
Interface for selecting contours in self.image
Assumes self.contours and self.hierarchy are defined and already detected and self.window_name is open to display selected contours on the image

A contour in OpenCV is a matrix of (x,y) points representing a boundary

The largest contour in self.contours at (x,y) is selected every time select_contour is ran, until two contours are selected, in which case the distances between the contours are measured and saved to self.json_data. The resulting measurements are visualized in self.window_name

In the future, this should presumably be changed to do the contour detection as well as selection, and to not be dependent on having an existing open window to visualize data. With those two changes it should be implementable in any user interface and only need the x,y points to measure between, but currently there are some steps in user_interface that are necessary for this to work.

Additionally, there are certainly better methods for selecting the 'best' contour than finding the largest one at that x,y point, as this function currently does. However, this is a necessary stopgap for now, as one x,y location may have many contours. In the future, it would be possible to use feature detection to specify which contour to measure.

## mouse_callback_wrapper(self):
Used to detect mouse input and pass the associated x/y points to select_contour, containing mouse_callback which is used by user_interface to interact with select_contours (since you can't change the parameters of mouse_callback this is the only way I know of to interact with member variables and mouse_callback)

## user_interface(self):
Opens a window to use EMU as standalone software. Connects to a camera, showing a live feed or using a set image instead if use_loaded_image is set to True. Opens a window showing the feed/image and starts a loop, which continually detects edges in the image and may be interrupted by pressing 'm' to enter measurement mode and select edges to measure between with mouse input.

Currently, user_interface does a lot of heavy lifting in as far as tasks that should be part of other functions (such as edge/contour detection) or could be other functions outright (such as some of the measurement loops)

# Dependencies/Running the Project

Instructions for using OpenCV with Python may be found at: 

https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

-Python 3.12
-numpy 2.1.2
-matplotlib 3.9.2
-opencv 4.10.0.84

# Credits / Further Reading
https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html
https://szeliski.org/Book/
https://calib.io/pages/camera-calibration-pattern-generator
