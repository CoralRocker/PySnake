#!/usr/bin/python
import curses
from curses import KEY_UP as UP, KEY_DOWN as DOWN

class Menu:
    def __init__(self):
        #Initialize Screen
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        self.scr = stdscr
        #Get Screen Size
        self.xy = list(stdscr.getmaxyx())
        self.xy.reverse()
        #Initialize Class Variables
        self.option = 0
        self.selection = -1
        self.title = 'NO TITLE INPUTTED'
        self.message = ['No Options']*3

    def DoMenu(self):
        while self.selection < 0:
            #Prep Screen
            self.scr.clear()
            #Start Option Choosing Mechanism
            g = [0]*len(self.message)
            g[self.option] = curses.A_REVERSE | curses.A_BOLD | curses.A_BLINK
            #Add Title to Screen
            self.scr.addstr(0, int(self.xy[0]/2-(len(self.title)/2)), self.title)
            #Add All Given Options to Screen
            for msg in range(0,len(self.message)):
                self.scr.addstr(int(self.xy[1]/2+msg), int(self.xy[0]/2-(len(self.message[msg])/2)), self.message[msg], g[msg])
            #Display Screen
            self.scr.refresh()
            #Get Key Input
            event = self.scr.getch()
            #Display Navigation and Get Selection
            if event == UP:
                self.option = (self.option - 1) % len(self.message)
            elif event == DOWN:
                self.option = (self.option + 1) % len(self.message)
            elif event == ord('\n'):
                self.selection = self.option

    def GetMenu(self, t, m):
        #Initialize Menu Variables
        self.title = t
        self.message = m
