#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:34:19 2019

@author: mtc-20
"""

import pygameMenu
import pygame
from auto_user_reg import *

# SETTTINGS
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255, 150, 10)
MENU_BACKGROUND_COLOR = (228, 55, 36)
COLOR_BACKGROUND = (20, 50, 30)

FPS = 30.0
WINDOW_SIZE = (640,480)
ABOUT = ['Autologger v0.1',
         'Author: @bathonSpidey, @mtc-20',
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: hsrwroboticsclub@gmail.com'.format(pygameMenu.__email__)]

clock = None
main_menu = None
screen = None
logo_rect = None
logo = None

def stets():
    pass

def main_bg():
    global screen
    screen.fill(BLACK)
    
    
def about_bg():
    global screen
    global logo
    global logo_rect
    #screen.fill(BLACK)
    screen.blit(logo, logo_rect)    
    

def main(test=False):
    # GLOBALS
    global standby
    global screen
    global clock
    global logo
    
    # INITIALIZATION
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    #screen.fill(BLACK)
    pygame.display.set_caption('Auto Logger')
    clock = pygame.time.Clock()
    
    logo = pygame.image.load('robotics_logo.png').convert()
    #img_lg = pygame.transform.scale(img, (75,75))
    logo_rect = logo.get_rect()
#    logo_rect.centerx = int(WINDOW_SIZE[0]/2)
#    logo_rect.centery = int(WINDOW_SIZE[1]/2)
    
    # MENUS
    new_user_menu = pygameMenu.Menu(surface=screen,bgfun=main_bg, color_selected=WHITE, font=pygameMenu.font.FONT_HELVETICA, window_width=int(WINDOW_SIZE[0]), window_height=int(WINDOW_SIZE[1]),menu_width=int(WINDOW_SIZE[0]), menu_height=int(WINDOW_SIZE[1]*0.5), onclose=pygameMenu.events.DISABLE_CLOSE, title='New User', font_color=BLACK, menu_color_title=ORANGE, menu_color=BLACK, menu_alpha=100, widget_alignment=pygameMenu.locals.ALIGN_LEFT, font_size=20)
    wid = new_user_menu.add_text_input('First Name: ', textinput_id='first_name', onreturn=add_new_user)
    
    about_menu = pygameMenu.TextMenu(surface=screen, bgfun=about_bg, color_selected=ORANGE, font=pygameMenu.font.FONT_BEBAS, window_width=WINDOW_SIZE[0], window_height=int(WINDOW_SIZE[1]), menu_color_title=ORANGE, menu_width=int(WINDOW_SIZE[0]*0.7), menu_height=int(WINDOW_SIZE[1]*0.7), text_fontsize=20, menu_alpha=0, onclose=pygameMenu.events.DISABLE_CLOSE, title='ABOUT', font_color=WHITE, menu_color=BLACK)
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to Menu', pygameMenu.events.BACK)
    
    standby = pygameMenu.Menu(surface=screen,bgfun=main_bg, color_selected=WHITE, font=pygameMenu.font.FONT_BEBAS, window_width=int(WINDOW_SIZE[0]), window_height=int(WINDOW_SIZE[1]),menu_width=int(WINDOW_SIZE[0]*0.8), menu_height=int(WINDOW_SIZE[1]*0.8), onclose=pygameMenu.events.DISABLE_CLOSE, title='Standby', font_color=BLACK, menu_color_title=WHITE, menu_color=ORANGE, menu_alpha=100)
    standby.add_option('Sign in', sign_in)
    standby.add_option('New user', new_user_menu)
    standby.add_option('About', about_menu)
    
    standby.set_fps(FPS)
    
    while True:
        clock.tick(FPS)
        main_bg()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
#        screen.blit()        
        screen.blit(logo, logo_rect)
        standby.mainloop(events, disable_loop=test)
        screen.blit(logo, logo_rect)
        pygame.display.flip()
        
        if test:
            break
        
if __name__ == '__main__':
    main()
        