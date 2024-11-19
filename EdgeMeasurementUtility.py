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

# Given:    Two 2D points
# Return:   The euclidean distance between them
def calculate_distance(pt1, pt2):
    return np.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)

# Given:    An image
# Return:   An edge-detected image
def detect_edges(image, min_val, max_val):
    print('Detecting edges...')
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    edges = cv.Canny(gray, min_val, max_val)
    
    return edges

# Given:    An image with a calibration target
# Return:   The ratio of millimeters to pixels in the image
def calibrate_mm_to_pixel_ratio():
    return 1

# Given:    A set of two contours and a desired direction (horizontal/vertical)
# Return:   The minimum and maximum distance between them in that direction
#            Ideally, this would also provide a visualization of these measurements
#           Or return a matrix representing them that can be used to visualize them
def measure_contour_distances():
    return 1

def mouse_callback(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        return (x,y)       

# to do:
    # move junk into functions
    # make it so the output image is more of the screen.. we dont need input
    # 
def user_interface():
    print('Initializing user interface')

    # ui parameters
    wait_time = 25
    height = 768
    width = 1360 
    panel_height = height 
    panel_width = width 
    window_name = 'Edge Measurement Utility'
    
    min_val = 127
    max_val = 200
    
    # environment states
    live_contours = True
    measurement_mode = False
    manual_measurement_mode = False
    
    # input keys
    live_contour_key = 'd'
    measurement_mode_key = 'm'
    manual_measurement_key = 'n'
    export_contours_key = 'c'

    ui_image = np.zeros((height, width, 3), np.uint8)    
    print('ui panel created')

    cv.namedWindow(window_name)

    cap = cv.VideoCapture(0)
    
    if not cap.isOpened():
        print('Unable to open camera')
        exit()
    
    # we need to determine some properties about the camera pre-loop
    ret, frame = cap.read()
    
    last_frame = frame
    
    f_height, f_width, channels = frame.shape
    
    scaling_factor_x = f_height // height
    scaling_factor_y = f_width // width 
    
    mm_pixel_ratio = calibrate_mm_to_pixel_ratio()

    while 1:
        print('looping...')
        
        if not measurement_mode:
            ret, frame = cap.read()
        else:
            frame = last_frame
        
        last_frame = frame

        if not ret:
            print('Unable to read frame')
            break

        edges = detect_edges(frame, min_val, max_val)

        print('Finding contours...')
        contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        print('Converting output to RGB...')
        edges_color = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)        

        if live_contours:
            print('Drawing contours...')
            cv.drawContours(edges_color, contours, -1, (0,255,0),2)
            
 #       print('Resizing input...')
 #       resized_input = cv.resize(frame, (panel_width, panel_height))
 #       resized_output = cv.resize(edges_color, (panel_width, panel_height))
 #       
 #       print('Modifying ui image...')
 #       ui_image[0:panel_height, 0:panel_width] = resized_input
 #       ui_image[0:panel_height, panel_width:width] = resized_output

        print('Resizing output to screen')
        resized_output = cv.resize(edges_color, (panel_width, panel_height))
        
        ui_image[0:panel_height, 0:panel_width] = resized_output

        print('Showing ui image...')
        cv.imshow(window_name, ui_image)
        
        print('Awaiting input...')
        # set up mouse callback if in measurement mode
        if measurement_mode:
            cv.setMouseCallback(window_name, mouse_callback)
            print('a')
            input_key = cv.waitKey(0)
            print('b')            
        else:
            input_key = cv.waitKey(wait_time) 
            print('c')
        

        if input_key & 0xFF == 27:
            break
        elif cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE) < 1:
            break
        elif input_key & 0xFF == ord(live_contour_key):
            live_contours = not live_contours
        elif input_key & 0xFF == ord(measurement_mode_key):
            measurement_mode = not measurement_mode
        elif input_key & 0xFF == ord(manual_measurement_key):
            manual_measurement_mode = not manual_measurement_mode


    print('Destroying windows and releasing camera')
    cap.release()
    cv.destroyAllWindows()
    
    print('Exit complete.')
    return 0
    
    
def main():
    user_interface()

if __name__ == "__main__":
    main()