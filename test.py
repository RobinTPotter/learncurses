import curses

screen = curses.initscr()
size = screen.getmaxyx()

import time
import threading

class Thing(threading.Thread):
    def __init__(self):
        super().__init__()
        self.count=50

    def run(self):
        while self.count>0:
            time.sleep(0.5)
            self.count -= 1

screen.nodelay(1)
curses.cbreak()
curses.noecho()
screen.keypad(1)
curses.curs_set(0)  # Turn cursor back on

thing = None

try:
    while True:
        screen.clear()
        c = screen.getch()
        if c>-1: screen.addstr(0,0,"You pressed keycode %d." % (c))

        if thing is None:
            if c==65:
                thing = Thing()
                thing.start()

        if thing is not None:
             if thing.is_alive():
                 screen.addstr(2,2,"x" * thing.count)
             else:
                 thing = None

             if c==66:
                 screen.addstr(2,2,"Cancelled")
                 thing.count=0
                 screen.addstr(3,2,"{} {}".format(thing,thing.is_alive()))

        screen.refresh()
        curses.napms(100)

finally:
    curses.nocbreak()   # Turn off cbreak mode
    curses.echo()       # Turn echo back on
    curses.curs_set(1)  # Turn cursor back on
    # If initialized like `my_screen = curses.initscr()`
    screen.keypad(0) # Turn off keypad keys
    curses.endwin()
