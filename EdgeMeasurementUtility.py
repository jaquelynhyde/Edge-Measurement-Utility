# Heliene USA Solar Panel Edge Measurement Utility

# Authors:

# Jaquelyn E Hyde
# jaquelyn.hyde@ire.minnstate.edu

# Elvis Enang

# Hannah Adeyemi

# Luhana Zorrilla

import numpy as np
import cv2 as cv
import json

class EdgeMeasurementUtility:
    def __init__(self):
        self.edges = None
        self.edges_color = None
        self.contours = None
        self.hierarchy = None
        self.selected_contours = []
        self.hor_contours = None
        self.ver_contours = None
        self.closest_hor_contour = None
        self.closest_ver_contour = None
        self.furthest_hor_contour = None
        self.furthest_ver_contour = None
        self.image = None
        self.last_image = None
        self.json_data = None
        self.mm_pixel_ratio = 1
        self.use_loaded_image = True
        self.loaded_image = cv.imread(cv.samples.findFile("Test_Image.jpg"))
        
    @staticmethod
    def horizontal_distance(point1, point2):
        return abs(point1[0] - point2[0])
        
    @staticmethod
    def vertical_distance(point1, point2):
        return abs(point1[1] - point2[1])
        
    # Given:    An image with a calibration target with (rows * cols) squares
    #           Each square's dimensions are (square_mm * square_mm) 
    # Return:   The ratio of millimeters to pixels in the image
    @staticmethod
    def calibrate_mm_to_pixel_ratio(image, rows, cols, square_mm):
        termination_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        objp = np.zeros((rows*cols,3), np.float32)
        objp[:,:2] = np.mgrid[0:rows,0:cols].T.reshape(-1,2)
        
        objpoints = [] # points in 3d space (real world)
        imgpoints = [] # points in 2d space (image plane)
        
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        ret, corners = cv.findChessboardCorners(gray, (rows, cols), None)
        
        if ret == True:
            objpoints.append(objp)
            
            corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), termination_criteria)
            
            imgpoints.append(corners2)
            
            total_horizontal_distance = 0
            total_vertical_distance = 0
            num_horizontal_distances = 0
            num_vertical_distances = 0
            
            for r in range(rows):
                for c in range(cols):
                    if c < cols - 1:
                        point1 = corners2[r * cols + c][0]
                        point2 = corners2[r * cols + c + 1][0]
                        distance = np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
                        total_horizontal_distance += distance
                        num_horizontal_distances += 1
                    if r < rows - 1:
                        point1 = corners2[r * cols + c][0]
                        point2 = corners2[(r + 1) * cols + c][0]
                        distance = np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
                        total_vertical_distance += distance
                        num_vertical_distances += 1 
                        
            average_horizontal_distance = total_horizontal_distance / num_horizontal_distances
            average_vertical_distance = total_vertical_distance / num_vertical_distances 
            average_distance = ( average_horizontal_distance + average_vertical_distance ) / 2
            average_distance_mm = square_mm / average_distance
            
            print('mm to pixel ratio : ' + str(average_distance_mm))
            
            return average_distance_mm
                
        return -1
    
    # Given:    An image
    # Return:   An edge-detected image    
    @staticmethod
    def detect_edges(image, min_val, max_val):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        edges = cv.Canny(gray, min_val, max_val)
        
        return edges
    
    # Placeholder for the portion of the utility that recognizes parts of the
    # solar panel and determines which contours belong to the components we are
    # interested in measuring
    def feature_detection():
        return 1
    
    # Interface for selecting contours in self.image based on x y location
    # The largest at x y is selected, to avoid selecting two with one click
    # When two contours are selected, measures distances between them/;'''''''''''''''''''''..
    def select_contour(self, x, y): 
        print('select_contour at x: ' + str(x) + ' / y: ' + str(y))   
        
        largest_idx = -1
        largest_area = -1

        for i, contour in enumerate(self.contours):
            if cv.pointPolygonTest(contour, (x, y), False) >= 0 and len(self.selected_contours) < 2:
                area = cv.contourArea(contour)
                if area > largest_area:
                    largest_idx = i
                    largest_area = area
                
        if largest_idx != -1 and len(self.selected_contours) < 2:
            self.selected_contours.append(largest_idx)
            cv.drawContours(self.image, self.contours[largest_idx], -1, (255, 255, 0), thickness = 3)
            cv.imshow(self.window_name, self.image)
            print('found contour! length is now: ' + str(len(self.selected_contours)))
            if len(self.selected_contours) == 2:
                contour1 = self.contours[self.selected_contours[0]]
                contour2 = self.contours[self.selected_contours[1]]                   
                    
                min_hor_dist = float('inf')
                max_hor_dist = float(0)
                min_ver_dist = float('inf')
                max_ver_dist = float(0)
                    
                closest_hor_points = None
                furthest_hor_points = None
                    
                closest_ver_points = None
                furthest_ver_points = None
                    
                for point1 in contour1:
                    for point2 in contour2:
                        if point1[0][1] == point2[0][1]:
                            dist = self.horizontal_distance(point1[0], point2[0])
                            if dist < min_hor_dist:
                                min_hor_dist = dist
                                closest_hor_points = (point1[0], point2[0])
                            if dist > max_hor_dist:
                                max_hor_dist = dist
                                furthest_hor_points = (point1[0], point2[0])
                        if point1[0][0] == point2[0][0]:
                            dist = self.vertical_distance(point1[0], point2[0])
                            if dist < min_ver_dist:
                                min_ver_dist = dist
                                closest_ver_points = (point1[0], point2[0])
                            if dist > max_ver_dist:
                                max_ver_dist = dist
                                furthest_ver_points = (point1[0], point2[0])
                                    
                if closest_hor_points:
                    self.closest_hor_contour = np.array([
                        closest_hor_points[0],
                        closest_hor_points[1],
                        (closest_hor_points[1][0], closest_hor_points[1][1] - 1),
                        (closest_hor_points[0][0], closest_hor_points[0][1] - 1)],
                        dtype = np.int32)
                    
                if closest_ver_points:
                    self.closest_ver_contour = np.array([
                        closest_ver_points[0],
                        closest_ver_points[1],
                        (closest_ver_points[1][0], closest_ver_points[1][1] - 1),
                        (closest_ver_points[0][0], closest_ver_points[0][1] - 1)],
                        dtype = np.int32)
                        
                if furthest_hor_points:
                    self.furthest_hor_contour = np.array([
                        furthest_hor_points[0],
                        furthest_hor_points[1],
                        (furthest_hor_points[1][0], furthest_hor_points[1][1] - 1),
                        (furthest_hor_points[0][0], furthest_hor_points[0][1] - 1)],
                        dtype = np.int32)
                        
                if furthest_ver_points:
                    self.furthest_ver_contour = np.array([
                        furthest_ver_points[0],
                        furthest_ver_points[1],
                        (furthest_ver_points[1][0], furthest_ver_points[1][1] - 1),
                        (furthest_ver_points[0][0], furthest_ver_points[0][1] - 1)],
                        dtype = np.int32)
                        
                if self.closest_hor_contour is not None:
                    cv.drawContours(self.image, [self.closest_hor_contour], -1, (0, 255, 255), thickness = cv.FILLED)
                    x, y, w, h = cv.boundingRect(self.closest_hor_contour)
                    cv.putText(self.image, 'closest horizontal distance : ' + str(min_hor_dist * self.mm_pixel_ratio) + ' mm', (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv.LINE_AA)
                        
                if self.closest_ver_contour is not None:
                    cv.drawContours(self.image, [self.closest_ver_contour], -1, (0, 255, 255), thickness = cv.FILLED)
                    x, y, w, h = cv.boundingRect(self.closest_ver_contour)
                    cv.putText(self.image, 'closest vertical distance : ' + str(min_ver_dist * self.mm_pixel_ratio) + ' mm', (0, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv.LINE_AA)
                        
                if self.furthest_hor_contour is not None:
                    cv.drawContours(self.image, [self.furthest_hor_contour], -1, (0, 0, 255), thickness = cv.FILLED)
                    x, y, w, h = cv.boundingRect(self.furthest_hor_contour)
                    cv.putText(self.image, 'furthest horizontal distance : ' + str(max_hor_dist * self.mm_pixel_ratio) + ' mm', (0, 90), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv.LINE_AA)
                        
                if self.furthest_ver_contour is not None:
                    cv.drawContours(self.image, [self.furthest_ver_contour], -1, (0, 0, 255), thickness = cv.FILLED)
                    x, y, w, h = cv.boundingRect(self.furthest_ver_contour)
                    cv.putText(self.image, 'furthest vertical distance : ' + str(max_ver_dist * self.mm_pixel_ratio) + ' mm', (0, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv.LINE_AA)
                        
                distances = { 
                    "min_horizontal_distance": float(min_hor_dist * self.mm_pixel_ratio),
                    "max_horizontal_distance": float(max_hor_dist * self.mm_pixel_ratio),
                    "min_vertical_distance": float(min_ver_dist * self.mm_pixel_ratio),
                    "max_vertical_distance": float(max_ver_dist * self.mm_pixel_ratio)
                    }
                    
                self.json_data = json.dumps(distances, indent=4)
                    
                print(json.dumps(distances, indent=4))
                    
                cv.imshow(self.window_name, self.image)

                        
    def mouse_callback_wrapper(self):
        def mouse_callback(event, x, y, flags, param):
            if event == cv.EVENT_LBUTTONDOWN:
                self.select_contour(x, y)
        return mouse_callback
    
    def user_interface(self):
        # ui parameters
        wait_time = 25
        
        self.window_name = 'Edge Measurement Utility'
        
        min_val = 127
        max_val = 200
        
        measurement_mode = False # toggle between live feed and measuring on an image
        
        measurement_mode_key = 'm'
        
        cv.namedWindow(self.window_name)

        cap = cv.VideoCapture(1)
        
        if not cap.isOpened():
            print('Unable to open camera')
            exit()
        
        # we need to determine some properties about the camera pre-loop
        ret, frame = cap.read()
        
        self.image = frame.copy()
        
        if self.use_loaded_image == True:
            self.image = self.loaded_image.copy()
            
        f_height, f_width, channels = frame.shape
        
        cv.resizeWindow(self.window_name, f_height, f_width)
        
        self.mm_pixel_ratio = self.calibrate_mm_to_pixel_ratio(self.image, 7, 10, 15)

        while True:            
            if not measurement_mode:
                self.selected_contours.clear()
                self.closest_hor_contour = None
                self.closest_ver_contour = None
                self.furthest_hor_contour = None
                self.furthest_ver_contour = None
                ret, frame = cap.read()
                if not ret:
                    print('Unable to read frame')
                    break
                
                self.image = frame.copy()
                
            if self.use_loaded_image == True:
                self.image = self.loaded_image.copy()
            
            self.edges = self.detect_edges(self.image, min_val, max_val)
            
            if measurement_mode:
                self.contours, self.hierarchy = cv.findContours(self.edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                self.edges_color = cv.cvtColor(self.edges, cv.COLOR_GRAY2BGR) 
                cv.drawContours(self.edges_color, self.contours, -1, (0,255,0), thickness = 1)
                print('Contours detected: ' + str(len(self.contours)))
            else:
                self.edges_color = cv.cvtColor(self.edges, cv.COLOR_GRAY2BGR) 
    
            self.image = self.edges_color

            cv.imshow(self.window_name, self.image)
            
            if measurement_mode:
                self.last_image = self.image
                cv.setMouseCallback(self.window_name, self.mouse_callback_wrapper())
                input_key = cv.waitKey(0)
            else:
                cv.setMouseCallback(self.window_name, lambda *args : None)
                input_key = cv.waitKey(wait_time)             

            if input_key & 0xFF == 27:
                break
            elif cv.getWindowProperty(self.window_name, cv.WND_PROP_VISIBLE) < 1:
                break
            elif input_key & 0xFF == ord(measurement_mode_key):
                measurement_mode = not measurement_mode

        print('Destroying windows and releasing camera')
        cap.release()
        cv.destroyAllWindows()
        
        print('Exit complete.')
        return 0
                        
if __name__ == "__main__":
    tool = EdgeMeasurementUtility()
    tool.user_interface()
