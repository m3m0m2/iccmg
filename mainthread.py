import threading
import menu
import curses
from logger import logger

class MainThread(threading.Thread):
  def __init__(self,input,stdscreen):
    super(MainThread, self).__init__()
    self.input = input
    self.screen = stdscreen
    curses.curs_set(0)

    self.menu_items = [
      ('Games', [
        ('Tetris', curses.beep),
        ('Tetris', 'bastet'),
        ('Snake', curses.flash)
      ]),
      ('TV', curses.beep),
      ('Radio', curses.beep)
    ]


  def run(self):
    while True:
      main_menu = menu.Menu(self.input, self.menu_items, self.screen, 0, 0)
      selection = main_menu.display()
      logger.info(self.__class__.__name__ + " selected:" + str(selection))
      if selection == 'CMD_QUIT':
        break
      #event = self.input.popWait(1)

