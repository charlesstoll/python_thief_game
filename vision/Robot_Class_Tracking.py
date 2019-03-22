import cv2
import numpy as np
import argparse
import imutils
import socket
import math

not_using_opencv = True
no_robots = False
p1_l = 1
p1_u = 2
p2_l = 3
p2_u = 4
t1_l = 5
t1_u = 6

class Robot_Track(object):
    def __init__(self, camera_index):
        self.cap = cv2.VideoCapture(camera_index)
        self.board_layout = {
                (0,0) : (444, 82),
                (1,0) : (351, 263),
                (1,1) : (452, 208),
                (1,2) : (558, 249),
                (2,0) : (286, 421),
                (2,1) : (365, 385),
                (2,2) : (467, 418),
                (2,3) : (557, 371),
                (2,4) : (653, 407),
                (3,0) : (231, 550),
                (3,1) : (306, 531),
                (3,2) : (385, 558),
                (3,3) : (469, 521),
                (3,4) : (559, 549),
                (3,5) : (640, 513),
                (3,6) : (710, 539)
                }

        
    def static_board_coords(self, row, column):
        #pull in current coords
        return self.board_layout[(row, column)]
            
    def get_location(self, name):
        #read in current contours 
        robot = name
        print(name)
    #get the HSV values for the robot based on name.
        if robot == 'p1':
            hsv_l = np.array([44, 52, 101])
            hsv_u = np.array([69, 255, 255])
            
        elif robot == 'p2':
            hsv_l = np.array([0, 125, 123])
            hsv_u = np.array([32, 255, 255])
        
        else:
            hsv_l = np.array([0, 49, 167])
            hsv_u = np.array([11, 105, 255])
            
        x, y = self.get_blob(name)
        return x, y
        
    def get_blob(self, robot):
        circles = []
        count = 0
        while (1):
            print("get_blob iter")
            ret, frame = self.cap.read()
            #gray_vid = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
            #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            kernel = np.ones((5,5), np.uint8)
            if robot == 'p1':
                lower_red = np.array([0, 128, 123])
                upper_red = np.array([19, 255, 255])
                
            elif robot == 'p2':
                lower_red = np.array([44, 52, 101])
                upper_red  = np.array([69, 255, 255])
            
            else:
                lower_red = np.array([0, 49, 167])
                upper_red = np.array([11, 255, 255])
     
            hsv_vid = cv2.morphologyEx(hsv_vid, cv2.MORPH_OPEN, kernel)
            #edged_frame = cv2.Canny(gray_vid, 150, 200, 5)
            #lower_red = hsv_low
            #upper_red = hsv_upper
            mask = cv2.inRange(hsv_vid, lower_red, upper_red)
            mask = cv2.erode(mask, kernel)
            mask = cv2.dilate(mask, kernel)
            #res = cv2.bitwise_and(edged_frame, edged_frame, mask = mask)
            gray = cv2.GaussianBlur(mask,(5,5),0)
            gray = cv2.medianBlur(gray, 5)

            rows = gray.shape[0]
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows/8,param1=100, param2=20, minRadius=10, maxRadius=40)
            if circles is not None:
                break
        if circles is not None:    
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                x = i[0]
                y = i[1]
                return x, y

    def move_robot(self, name, ip, row, col):
        if(not_using_opencv):
            good = 0
            while good == 0:
                print("please give directions for the robot " + name + "to get to location (" + str(row) + "," + str(col) +")")
                distance = float(input("Distance:  "))
                if name == "t":
                    distance = int(distance)
                angle = int(input("Angle:  "))
                self.send_message(name, ip, angle, distance)
                good = int(input("is he in the right spot? (1/0)  "))
            return
                #get contour and centroid for dest
        r1_row, r1_col =  self.get_location(name)
        dest_row, dest_col = self.static_board_coords(row, col)
        
                #calculate angle and distance for robot move
        print("dst col: " + str(dest_col) + " dst row: " + str(dest_row))
        print("r1 col: " + str(r1_col) + " r1 row: " + str(r1_row))
        angle  = math.degrees(math.atan2((dest_row - r1_row), (r1_col - dest_col)))
        distance = math.sqrt((dest_row - r1_row)**2 + (r1_col - dest_col)**2)
        # send the message
        print("robot " + name + "to get to location (" + str(row) + "," + str(col) +")")
        self.send_message(name, ip, angle, distance)

    def send_message(self, name, ip, angle, distance):

        angle = int(angle)
        if(angle < 0):
            angle = angle + 360

        if(name == "t"):
            distance = int(distance)

        elif(name == "p1"):
            distance = distance

        else:
            distance = distance
        
        if(no_robots):
            print("sending robot: " + str(name) + " dist: " + str(distance) + " angle: " + str(angle))
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("sending robot: " + str(name) + " dist: " + str(distance) + " angle: " + str(angle))

        server_address = (ip, 65432)
        sock.connect(server_address)

        message = "{0},{1}".format(angle, distance)
        sock.sendall(message.encode('ascii'))

        data = sock.recv(3)
        sock.close()
        
    def current_board(self):
        #get image data for current game board
        #this function may be obsolete if other options work
        for i in range (0, 9):
            ret, frame = self.cap.read()
            gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
                    
            kernel = np.ones((6,6), np.uint8)
            nois_reduce = cv2.morphologyEx(gray_vid, cv2.MORPH_OPEN, kernel)
            edged_frame = cv2.Canny(nois_reduce, 150, 200, 5)

            _, threshold = cv2.threshold(edged_frame, 150, 200, 0)
            im2, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    
            for cnt in contours:
                approx = cv2.approxPolyDP(cnt, 0.07*cv2.arcLength(cnt, True), True)
                M = cv2.moments(cnt)
                            
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    if len(approx) == 3:
                        cv2.circle(nois_reduce, (cX, cY), 5, (255), -1)
                else:
                    cX, cY = 0, 0
                    
            #denoised = cv2.GaussianBlur(edged_frame,(5,5),0)
            #Testing finding triangles:
            #triangles = find_triangles(edged_frame)
                    
            cv2.imshow('Original',frame)
            cv2.imshow('Contours and edges',nois_reduce)
                    
            k = cv2.waitKey(5)
    
    
