#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 19:47:51 2019

@author: mtc-20
"""

import pickle
import cv2
import face_recognition

# To create the file the first time when there are already existing users
#workers=['Abir','Quang', 'Thomas', 'Prof Hartanto']
#with open('users.txt', 'wb') as f:
#    pickle.dump(workers, f)

# Add block to check for existence of file
    
# This assumes the file already exists    
with open('users.txt', 'rb') as f:
    users = pickle.load(f) 
    
with open('encodings.txt', 'rb') as f:
    known_face_encodings = pickle.load(f)

def save_image(name):
    print("[INFO] Loading camera...")
    cap = cv2.VideoCapture(0)
    width  = int(cap.get(cv2.cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(width, height)
    
    # Specify ROI coordinates
    x1, y1 = int(width/4), int(height/4)
    x2, y2 = int(width*3/4), int(height*3/4)
    while True:
        ret, frame = cap.read()
        if ret is None:
            print("[INFO] No feed found...")
            print("Exiting!")
            chk = False
            break
        roi = frame[(y1 + 5):(y2 -5), int(x1 + 5):int(x2 - 5)]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (200,0,0), 3)
        text = "Ensure entire face is positioned \n within the rectangle \n and press SPACE to confirm"
        
        y0, dy = (height - 80), 30
        for i, line in enumerate(text.split('\n')):
            y = y0 + i*dy
            cv2.putText(frame, line, (50, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,0,0), 2)
            
        cv2.imshow('frame', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            chk = False
            print("[INFO] Exiting...")
            break
        elif k ==32:
            #name = 'Thomas'
            img_name = "{}.jpg".format(name)
            cv2.imwrite(img_name, roi)
            print("{}'s Visual ID written!".format(img_name))
            chk = True
            break
    cap.release()
    cv2.destroyAllWindows()
    return chk




    
    
def add_new_user():
    # username entry
    name = input("Please enter first name: ")
        
    while name in users:
        print("Username [%s] already exists!!!" % name)
        print("Please try again!")
        name = input("Please enter first name: ")
    
    print("[INFO] No duplicate found, proceeding...")
    
    #cap = cv2.VideoCapture(0)
    
#    result = save_image(name)
    # extract encodings
    if save_image(name):
        image_path = "faces/{}.jpg".format(name)
        img = face_recognition.load_image_file(image_path)
        encoding=face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoding)
        users.append(name)
        
        print("[INFO] Registering user to database...")
    
        with open('users.txt', 'wb') as f:
            pickle.dump(users, f)
        
        with open('encodings.txt', 'wb') as f:
            pickle.dump(known_face_encodings, f)

        # Check updated files      
        with open('users.txt', 'rb') as fp:
            print(pickle.load(fp))
    
    else:
        print("[INFO] User registration interrupted...")
        
    
#try:    
#    add_new_user()
#except: 
#    pass        