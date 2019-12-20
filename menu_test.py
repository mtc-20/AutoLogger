#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:34:19 2019

@author: mtc-20
"""

import os
import pygameMenu
import pygame
from auto_user_reg import *
import face_recognition

# SETTTINGS
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255, 150, 10)
MENU_BACKGROUND_COLOR = (228, 55, 36)
COLOR_BACKGROUND = (20, 50, 30)

FPS = 10
WINDOW_SIZE = (640,480)
ABOUT = ['Autologger v0.1',
         'Author: @Spidey, @mtc-20',
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: hsrwroboticsclub@gmail.com']

# Set window position
x = 50
y = 20
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

clock = None
main_menu = None
screen = None
#background = None

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
    screen = pygame.display.set_mode(WINDOW_SIZE)
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
            break
        
if __name__ == '__main__':
    main()
        