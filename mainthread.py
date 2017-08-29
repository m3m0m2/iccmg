import threading
import menu
import curses
from logger import logger
import childprocess
import time

class MainThread(threading.Thread):
  def __init__(self,input,stdscreen,child):
    super(MainThread, self).__init__()
    self.input = input
    self.screen = stdscreen
    self.child = child
    curses.curs_set(0)

    # curses.beep, curses.flash
    self.menu_items = [
      ('Games', [
        ('Tetris', 'bastet'),
        ('Snake', 'games/snake.py')
      ]),
      ('TV', curses.beep),
      ('Radio', curses.beep)
    ]

  def stop(self):
    pass


  def run(self):
    while True:
      logger.info(self.__class__.__name__ + " starting Menu")
      main_menu = menu.Menu(self.input, self.menu_items, self.screen, 0, 0)
      selection = main_menu.display()
      if selection.isCmd('CMD_QUIT'):
        break
      if selection != None: 
        logger.info(self.__class__.__name__ + " selected:" + str(selection) + ", context: " + str(selection.getContext()))
        if selection.getContext()[0] == 'Games':
          self.child.start(selection.getCmd())
          while self.child.isRunning():
            time.sleep(0.5)
      #event = self.input.popWait(1)

