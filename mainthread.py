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
      ('Media', self.video.getMenu()),
      ('Settings', [
        ('Video', self.video.getSettingsMenu())
      ])
    ]

  def stop(self):
    self.radio.stop()


  def run(self):
    self.updateMenu()
    logger.info(self.__class__.__name__ + " starting Menu")
    main_menu = menu.Menu(self.input, self.menu_items, self.screen, 0, 0)

    while True:
      ret = None
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
        self.input.clear()
        self.input.setActiveInput(True)
        time.sleep(2)
        ret = self.radio.handleInput(self.input)
        self.input.setActiveInput(False)
        # Radio could maybe run as a background process
      elif selection.getContext()[0] == 'Sat':
        self.sat.start(selection.getCmd())
        self.input.clear()
        self.input.setActiveInput(True)
        time.sleep(3)
        ret = self.sat.handleInput(self.input)
        self.input.setActiveInput(False)
      elif selection.getContext()[0] == 'Media':
        self.video.start(selection.getCmd())
        self.input.clear()
        self.input.setActiveInput(True)
        time.sleep(1)
        ret = self.video.handleInput(self.input)
        self.input.setActiveInput(False)
      if ret == 'CMD_QUIT':
        break
    self.stop()

