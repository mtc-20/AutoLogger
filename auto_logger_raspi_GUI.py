#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:34:19 2019

@author: mtc-20

TODO: check logic for multiple entry; currently only signs in
TODO: event callbacks logic needs to be rectfied; eg. if user double clicks 'Sign in' accidently, then the function is also called twice (added to queue)
"""

import pickle
import cv2
import numpy as np
import os
import glob
from datetime import datetime
import math
import time

start = time.time()
import pygameMenu
import pygame
end = time.time()
print("[INFO] Time to load pygame and pygame-menu: %.3f" %(end - start))
start = time.time()
import face_recognition
end = time.time()
print("[INFO] Time to load face_recognition: %.3f" %(end - start))

# SETTINGS
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255, 150, 10)
MENU_BACKGROUND_COLOR = (228, 55, 36)
COLOR_BACKGROUND = (20, 50, 30)


FPS = 10
WINDOW_SIZE = (640,480)
ABOUT = ['Autologger v0.1',
         'Author: @Spidey, @mtc-20, @quangnhat185',
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: hsrwroboticsclub@gmail.com']

# Set window position
x = 0
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

clock = None
main_menu = None
screen = None
#background = None

# Add block to check for existence of file


# This assumes the file already exists
print("[INFO] Loading user database...")
with open('users.txt', 'rb') as f:
    known_face_names = pickle.load(f)

with open('encodings.txt', 'rb') as f:
    known_face_encodings = pickle.load(f)
print(known_face_names)

# FUNCTION DEFINITIONS
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

    # INITIALIZATION
    process_this_frame = True
    count=0
    entry = ''
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

    # DATA LOGGING TO FILE
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

# test function
def fun():
    print('fun')
    pass

def main_bg():
    global screen
    screen.fill(BLACK)
#    screen.blit(background, background_rect)


#def about_bg():
#    global screen
#    screen.fill(BLACK)
##    screen.blit(background, background_rect)


def main(test=False):
    # GLOBALS
    global standby
    global screen
    global clock
    global background
    global background_rect

    # INITIALIZATION
    pygame.init()
    info = pygame.display.Info()
    WINDOW_SIZE = (info.current_w, info.current_h)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # # To be used for final build (No close window buttons)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #screen.fill(BLACK)
    pygame.display.set_caption('Auto Logger')
    clock = pygame.time.Clock()
#    background = pygame.image.load('robotics_logo.png').convert()
#    background = pygame.transform.scale(background, (70,55))
#    background_rect = background.get_rect()
#    background_rect.centerx = WINDOW_SIZE[0]/2
#    background_rect.centery = WINDOW_SIZE[1]/2

    # MENUS
    new_user_menu = pygameMenu.Menu(surface=screen,bgfun=main_bg, color_selected=WHITE, font=pygameMenu.font.FONT_HELVETICA, window_width=int(WINDOW_SIZE[0]), window_height=int(WINDOW_SIZE[1]),menu_width=int(WINDOW_SIZE[0]*0.9), menu_height=int(WINDOW_SIZE[1]*0.5), onclose=pygameMenu.events.DISABLE_CLOSE, title='New User', font_size_title= 40, font_title=pygameMenu.font.FONT_BEBAS, font_color=BLACK, menu_color_title=ORANGE, menu_color=BLACK, menu_alpha=100, widget_alignment=pygameMenu.locals.ALIGN_LEFT, font_size=20)
    wid1 = new_user_menu.add_text_input('First Name: ', input_underline='.', maxchar=20, onreturn=add_new_user)

    confirm_signin = pygameMenu.Menu(surface=screen,bgfun=main_bg, color_selected=WHITE, font=pygameMenu.font.FONT_FRANCHISE, window_width=int(WINDOW_SIZE[0]), window_height=int(WINDOW_SIZE[1]),menu_width=int(WINDOW_SIZE[0]*0.9), menu_height=int(WINDOW_SIZE[1]*0.5), onclose=pygameMenu.events.DISABLE_CLOSE, font_title=pygameMenu.font.FONT_BEBAS, title='Sign In', font_color=BLACK, menu_color_title=ORANGE, menu_color=BLACK, menu_alpha=100,  font_size=40)
    confirm_signin.add_option('Please click once to confirm sign-in attempt', sign_in)

    about_menu = pygameMenu.TextMenu(surface=screen, bgfun=main_bg, color_selected=ORANGE, font=pygameMenu.font.FONT_BEBAS, window_width=WINDOW_SIZE[0], window_height=int(WINDOW_SIZE[1]), menu_color_title=ORANGE, menu_width=int(WINDOW_SIZE[0]*0.7), menu_height=int(WINDOW_SIZE[1]*0.7), text_fontsize=20, menu_alpha=100, onclose=pygameMenu.events.DISABLE_CLOSE, title='ABOUT', font_color=WHITE, menu_color=BLACK)
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to Menu', pygameMenu.events.BACK)

    standby = pygameMenu.Menu(surface=screen,bgfun=main_bg, color_selected=WHITE, font=pygameMenu.font.FONT_FRANCHISE, window_width=int(WINDOW_SIZE[0]), window_height=int(WINDOW_SIZE[1]),menu_width=int(WINDOW_SIZE[0]*0.8), menu_height=int(WINDOW_SIZE[1]*0.8), onclose=pygameMenu.events.DISABLE_CLOSE, title='Main Menu', font_color=BLACK, menu_color_title=WHITE, menu_color=ORANGE, menu_alpha=100)
    standby.add_option('Sign In', confirm_signin)
    standby.add_option('New User', new_user_menu)
    standby.add_option('Test Button', fun)
    standby.add_option('About', about_menu)

    standby.set_fps(FPS)

    while True:
        clock.tick(FPS)
        main_bg()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        standby.mainloop(events, disable_loop=test)
        pygame.display.flip()

        if test:
            print("[INFO] Exitting system...")
            break

if __name__ == '__main__':
    main()
