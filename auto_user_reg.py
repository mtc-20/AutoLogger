#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 19:47:51 2019

@author: mtc-20
"""

import pickle
import cv2
#import face_recognition

import cv2
import numpy as np
import os
import glob
from datetime import datetime
import math
import time

# To create the file the first time when there are already existing users
#workers=['Abir','Quang', 'Thomas', 'Prof Hartanto']
#with open('users.txt', 'wb') as f:
#    pickle.dump(workers, f)

# Add block to check for existence of file
    
# This assumes the file already exists    
with open('users.txt', 'rb') as f:
    known_face_names = pickle.load(f) 
    
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




    
    
def add_new_user(name):
    # username entry
    #name = input("Please enter first name: ")
        
    if name in known_face_names:
        print("Username [%s] already exists!!!" % name)
        print("Please try again!")
#        name = input("Please enter first name: ")
        return None
    
    print("[INFO] No duplicate found, proceeding...")
    
    #cap = cv2.VideoCapture(0)
    
#    result = save_image(name)
    # extract encodings
    if save_image(name):
        image_path = "faces/{}.jpg".format(name)
        img = face_recognition.load_image_file(image_path)
        encoding=face_recognition.face_encodings(img)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(name)
        
        print("[INFO] Registering user to database...")
    
        with open('users.txt', 'wb') as f:
            pickle.dump(known_face_names, f)
        
        with open('encodings.txt', 'wb') as f:
            pickle.dump(known_face_encodings, f)

        # Check updated files      
        with open('users.txt', 'rb') as fp:
            print(pickle.load(fp))
    
    else:
        print("[INFO] User registration interrupted...")
        
def sign_in():
    print("[INFO] Loading user database...")
    print(known_face_names)
    
    # Initialization
    process_this_frame = True
    count=0
    entry = ''
#    workers=['Abir','Quang', 'Thomas', 'Prof Hartanto'] 
    name='dummy'
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.cv2.CAP_PROP_FPS, 2)

    while True:

        # Grab a single frame of video
        ret, frame = video_capture.read()
    
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
    
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
    
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]
    
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
    
                face_names.append(name)
    
        process_this_frame = not process_this_frame
    
    
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
    
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if name in known_face_names:
            count+=1
            if count==5:
                entry += 'in'
                break
        # Display the resulting image
        cv2.imshow('Video', frame)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    
    # Data Logger
    # TODO: should a person be allowed to log-in multiple times???
    # 

    now=datetime.now()
    log=os.listdir('logbook/')
    month=now.strftime("%B")
    year=str(now.year)
    day=str(now.day)
    hour=str(now.hour)
    minute=str(now.minute)
    print(log)


    if month+' '+year not in log:
        os.mkdir('logbook/'+(now.strftime("%B")+' '+year))
    day_glob=os.listdir("logbook/"+month+' '+year)
    print(day_glob)
    file_path="logbook/"+(now.strftime("%B")+' '+year)
    file_name=day+'-'+month+'-'+year+'.txt'
    full_path=os.path.join(file_path, file_name)
    if day+'-'+month+'-'+year+'.txt' not in day_glob: # create new file? Then check out shouldn't happen
        f=open(full_path,"a+")
        if 'in' in entry:
            f.write('[Check In++] Username: '+name+' '+day+'-'+ str(now.month) +'-'+year+' '+ str(now.strftime("%H:%M"))+'\n')
        
    else:
        f=open(full_path,"r")                       # 
        a=f.read()
        #f=open(full_path,"a+")
        if 'in' in entry:
            if '[Check In++] Username: '+name in a and '[--Check Out] Username: '+name not in a:
                print('You are already in. Logging you out now')
                g=open(full_path,"a+")
                g.write('[--Check Out] Username: '+name+' '+day+'-'+ str(now.month) +'-'+year+' '+str(now.strftime("%H:%M"))+'\n')
                g.close()
            else:
                g=open(full_path,"a+")
                g.write('[Check In++] Username: '+name+' '+day+'-'+ str(now.month) +'-'+year+' '+ str(now.strftime("%H:%M"))+'\n')
                g.close()
        else:
            if '[--Check Out] Username: '+name in a:
                print('You are already out. Try again with fist bump to come in')
            else:
                 g=open(full_path,"a+")
                 g.write('[--Check Out] Username: '+name+' '+day+'-'+ str(now.month) +'-'+year+' '+str(now.strftime("%H:%M"))+'\n')
                 g.close()
        
    f.close()
    

    
#try:    
#    add_new_user()
#except: 
#    pass        