import threading
import menu
import curses
from logger import logger
import childprocess
import time
from radio import Radio
from video import Video 
from sat import Sat

class MainThread(threading.Thread):
  def __init__(self,input,stdscreen,child):
    super(MainThread, self).__init__()
    self.input = input
    self.screen = stdscreen
    self.child = child
    curses.curs_set(0)
    self.radio = Radio()
    self.video = Video()
    self.sat = Sat()

  def updateMenu(self):
    # curses.beep, curses.flash
    self.menu_items = [
      ('Games', [
        ('Tetris', 'bastet'),
        ('Snake', 'games/snake.py')
      ]),
      ('Radio', self.radio.getMenu()),
      ('Sat', self.sat.getMenu()),
      ('Settings', [
        ('Video', self.video.getMenu())
      ])
    ]

  def stop(self):
    self.radio.stop()


  def run(self):
    self.updateMenu()
    while True:
      logger.info(self.__class__.__name__ + " starting Menu")
      main_menu = menu.Menu(self.input, self.menu_items, self.screen, 0, 0)
      self.input.clear()
      self.input.setActiveInput(True)
      selection = main_menu.display()
      self.input.setActiveInput(False)
      if selection is None: 
        continue

      if selection.isCmd('CMD_QUIT'):
        break
      logger.info(self.__class__.__name__ + " selected:" + str(selection) + ", context: " + str(selection.getContext()))
      if selection.getContext()[0] == 'Games':
        self.child.start(selection.getCmd())
        while self.child.isRunning():
          time.sleep(0.5)
      elif selection.getContext()[0] == 'Radio':
        self.radio.start(selection.getCmd())
        # Radio can run as a background process
        #while self.radio.isRunning():
        #  time.sleep(0.5)
      elif selection.getContext()[0] == 'Sat':
        self.sat.start(selection.getCmd())
      #event = self.input.popWait(1)
    self.stop()

