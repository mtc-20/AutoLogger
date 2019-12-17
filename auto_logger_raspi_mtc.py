# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:59:49 2019

@author: spidey, mtc-20
"""
#LD_PRELOAD='/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python3'
import time
start= time.time()
import face_recognition
end = time.time()
import cv2
import numpy as np
import os
import glob
from datetime import datetime
import math
#import time
import pickle

print("Time to load lib: %.2f" %(end - start)) 
faces=glob.glob("faces/*.jpg")
#print(faces)
#print(faces[0].find('.'))
#print(faces[0][5+1:10])
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
known_face_encodings=[]
known_face_names=[]
#start = time.time()
#for face in faces:
#    image=face_recognition.load_image_file(face)
#    encoding=face_recognition.face_encodings(image)[0]
#    known_face_encodings.append(encoding)
#    slash_ind=face.find('/')
#    dot_index=face.find('.')
#    known_face_names.append(face[slash_ind+1:dot_index])
#end = time.time()
#print("Time to load database: %.2f" %(end - start))

start = time.time()
#with open('users.txt', 'wb') as f:
#    pickle.dump(known_face_names, f)


#with open('encodings.txt', 'wb') as f:
#    pickle.dump(known_face_encodings, f)

with open('users.txt', 'rb') as f:
    known_face_names = pickle.load(f)

with open('encodings.txt', 'rb') as f:
    known_face_encodings = pickle.load(f)

end = time.time()
print("Time to read from file: %.2f" %(end - start)) 
print(known_face_names)
#print(len(known_face_encodings),type(known_face_encodings))    
# Load a sample picture and learn how to recognize it.
'''
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
abir_image = face_recognition.load_image_file("abir.jpg")
abir_face_encoding = face_recognition.face_encodings(abir_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    abir_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Abir"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
'''
while True:
    process_this_frame = True
    count=0
    workers=['Abir','Quang', 'Thomas', 'Prof Hartanto']
    name='dummy'

    user_input=input('Press y and [ENTER] to use me: ')
    if user_input=='y':
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.cv2.CAP_PROP_FPS, 1)
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
            if name in workers:
                count+=1
                if count==5:
                    break
            # Display the resulting image
            cv2.imshow('Video', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


        #Putting coming in and going out logic
        time.sleep(2)
        cap = cv2.VideoCapture(0)
        cap.set(cv2.cv2.CAP_PROP_FPS, 24)
        entry=''  
        count_in=0
        count_out=0
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.moveWindow('frame', 30, 40)
        while(True):
            try:    
                ret, frame = cap.read()
                frame=cv2.flip(frame,1)
                kernel = np.ones((3,3),np.uint8)
                
                #define region of interest
                roi=frame[100:300, 100:300]
                
                
                cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)    
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                
                
                 
            # define range of skin color in HSV
                lower_skin = np.array([0,20,70], dtype=np.uint8)
                upper_skin = np.array([20,255,255], dtype=np.uint8)
                
             #extract skin colur imagw  
                mask = cv2.inRange(hsv, lower_skin, upper_skin)
                
               
                
            #extrapolate the hand to fill dark spots within
                mask = cv2.dilate(mask,kernel,iterations = 4)
                
            #blur the image
                mask = cv2.GaussianBlur(mask,(5,5),100) 
                
                
                
            #find contours
                contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
               #find contour of max area(hand)
                cnt = max(contours, key = lambda x: cv2.contourArea(x))
                
            #approx the contour a little
                epsilon = 0.0005*cv2.arcLength(cnt,True)
                approx= cv2.approxPolyDP(cnt,epsilon,True)
               
                
            #make convex hull around hand
                hull = cv2.convexHull(cnt)
                
             #define area of hull and area of hand
                areahull = cv2.contourArea(hull)
                areacnt = cv2.contourArea(cnt)
              
            #find the percentage of area not covered by hand in convex hull
                arearatio=((areahull-areacnt)/areacnt)*100
            
             #find the defects in convex hull with respect to hand
                hull = cv2.convexHull(approx, returnPoints=False)
                defects = cv2.convexityDefects(approx, hull)
                
            # l = no. of defects
                l=0
                
            #code for finding no. of defects due to fingers
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])
                    pt= (100,180)
                    
                    
                    # find length of all sides of triangle
                    a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                    b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                    c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                    s = (a+b+c)/2
                    ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
                    
                    #distance between point and convex hull
                    d=(2*ar)/a
                    
                    # apply cosine rule here
                    angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                    
                
                    # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                    if angle <= 90 and d>30:
                        l += 1
                        cv2.circle(roi, far, 3, [255,0,0], -1)
                    
                    #draw lines around hand
                    cv2.line(roi,start, end, [0,255,0], 2)
                    
                    
                l+=1
                
                #print corresponding gestures which are in their ranges
                font = cv2.FONT_HERSHEY_SIMPLEX
                if l==1:
                    if areacnt<2000:
                        cv2.putText(frame,'Put rock or best of luck for coming in and any other for going out inside the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    else:
                        if arearatio<12:
                            cv2.putText(frame,'Log in please wait...',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                            count_in+=1
                        elif arearatio<17.5:
                            cv2.putText(frame,'Log in registering...',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                            count_in+=1
                           
                        else:
                            cv2.putText(frame,'Could not recognize try again',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                            
                elif l==2:
                    cv2.putText(frame,'Could not recognize try again',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                elif l==3:
                 
                      if arearatio<27:
                            cv2.putText(frame,'Could not recognize try again',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                      else:
                            cv2.putText(frame,'Could not recognize try again',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                            
                elif l==4:
                    cv2.putText(frame,'Going out registered',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    count_out+=1
                    
                elif l==5:
                    cv2.putText(frame,'Going out registered',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    count_out+=1
                    
                elif l==6:
                    cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                else :
                    cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
                if count_in==50:
                    entry+='in'
                    break
                elif count_out==20:
                    entry+='out'
                    break
                    
                #show the windows
                cv2.imshow('mask',mask)
                cv2.imshow('frame',frame)
            except:pass
            
            if cv2.waitKey(1) & 0xFF == ord('q'):break
            
        cv2.destroyAllWindows()
        cap.release()   












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
        if day+'-'+month+'-'+year+'.txt' not in day_glob:
            f=open(full_path,"a+")
            if 'in' in entry:
                f.write('[Check In++] Username: '+name+' '+day+'-'+ str(now.month) +'-'+year+' '+ str(now.strftime("%H:%M"))+'\n')
            else:
                f.write('[--Check Out] Username: '+name+' '+day+'-'+ str(now.month) +'-'+year+' '+str(now.strftime("%H:%M"))+'\n') 
        else:
            f=open(full_path,"r")
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
    else:
        pass
