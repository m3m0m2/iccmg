import curses                                                                
import string
from curses import panel                                                     
from logger import logger

class MenuSelection:
  def __init__(self, cmd):
    self.cmd = cmd
    self.context = []

  def getCmd(self):
    return self.cmd

  def isCmd(self, cmd):
    return self.cmd == cmd

  def getContext(self):
    return self.context

  def pushContext(self, value):
    self.context.insert(0, value)

  def __str__(self):
    return str(self.getCmd())

class MenuView:
  def __init__(self, y, x, maxY, maxX):
    self.x = x
    self.y = y
    self.items = []

    minWidth = 10
    maxWidth = maxX - x
    if maxWidth < minWidth and x > 0:
      x = maxX - minWidth
      if x < 0:
        x = 0
      maxWidth = maxX - x
    self.maxWidth = maxWidth

    minHeight = 6
    maxHeight = maxY - y
    if maxHeight < minHeight and y > 0:
      y = maxY - minHeight
      if y < 0:
        y = 0
      maxHeight = maxY - y
    self.maxHeight = maxHeight

    self.currentIdx = 0
    self.width = 0
    self.height = 0
    self.topIdx = 0
    self.marginx = 2
    self.marginy = 2

  def addItem(self, item):
    self.items.append(item)

  def getItemText(self, i):
    item = self.items[i]
    if len(item) > 2:
      msg = '%d. [%s] %s' % (i + 1, 'X' if item[2]() else ' ', item[0])
    else:
      msg = '%d. %s' % (i + 1, item[0])
    msg = filter(lambda x: x in string.printable, msg)
    if len(msg) > (self.maxWidth - self.marginx):
      msg = msg[0:self.maxWidth - 3 - self.marginx] + '...'
    if self.width > (len(msg)+1):
      msg += ' ' * (self.width - len(msg)-1)
    if isinstance(item[1], Menu):
      msg += '>'
    else:
      msg += ' '
    return msg


  def calcSize(self):
    for i in range(len(self.items)):
      width=len(self.getItemText(i))
      if width > self.width:
        self.width = width
    self.height = len(self.items)
    if self.height > (self.maxHeight - self.marginy):
      self.height = self.maxHeight - self.marginy

  def getCurrentSelection(self):
    if self.currentIdx < len(self.items):
      return self.items[self.currentIdx]
    return None

  def parseKey(self, key):
    if key.isKey('KEY_UP'):
      if self.currentIdx > 0:
        self.currentIdx -= 1
        if self.topIdx > self.currentIdx:
          self.topIdx = self.currentIdx
      return True #key consumed
    elif key.isKey('KEY_DOWN'):
      if self.currentIdx < (len(self.items)-1):
        self.currentIdx += 1

        minTop = self.currentIdx - self.height + 1
        if self.currentIdx < (len(self.items)-1):
          minTop += 1
        if minTop > 0:
          minTop += 1

        if minTop > self.topIdx:
          self.topIdx = minTop

      return True #key consumed
    return False

  def createWindow(self,stdscreen):
    self.stdscreen = stdscreen
    self.calcSize()
    self.window = self.stdscreen.subwin(self.height + 2,self.width + 2,self.y,self.x)
    self.window.keypad(1)
    self.panel = panel.new_panel(self.window)
    self.panel.hide()
    panel.update_panels()

  def hasTopElipses(self):
    return self.topIdx > 0

  def hasBottomElipses(self):
    pos = self.topIdx + self.height
    if self.hasTopElipses():
      pos -= 1
    return pos < len(self.items)
    
  def hide(self):
    self.window.clear()
    self.panel.hide()
    panel.update_panels()
    curses.doupdate()

  def show(self):
    self.panel.top()
    self.panel.show()
    self.window.clear()
    self.window.box()

    self.calcSize()
    i = 0
    curIdx = self.topIdx
    mode = curses.A_NORMAL

    if self.hasTopElipses():
      line = '^' * self.width
      self.window.addstr(1+i, 1, line, mode)
      i += 1
    while i<self.height:
      if i==(self.height-1) and self.hasBottomElipses():
        line = '.' * self.width
      else:
        line = self.getItemText(curIdx)
      if self.currentIdx == curIdx:
        mode = curses.A_REVERSE
      else:
        mode = curses.A_NORMAL
      self.window.addstr(1+i, 1, line, mode)
      curIdx += 1
      i += 1

    self.window.refresh()
    curses.doupdate()
    




class Menu(object):                                                          

    def __init__(self, input, items, stdscreen, y, x):
        self.input = input
        #[ rows, cols ] = self.menuSize(items)
        #self.window = stdscreen.subwin(rows + 2,cols + 5,levely,levelx)
        #self.window.keypad(1)
        #self.panel = panel.new_panel(self.window)
        #self.panel.hide()
        #panel.update_panels()
        [maxy, maxx] = stdscreen.getmaxyx()
        self.view = MenuView(y,x,maxy-2,maxx-2)

        #self.position = 0
        #self.items = items
        for i in range(len(items)):
          item = items[i]
          self.view.addItem(item)
        self.view.createWindow(stdscreen)

        #create submenu after parent window sizes are known
        for i in range(len(items)):
          item = items[i]
          if type(item[1]) is list:
            submenu = Menu(self.input, item[1], stdscreen, y + i, x + 2 + self.view.width)
            item = (item[0], submenu)
            self.view.items[i] = item
       

    def display(self):
        #self.panel.top()
        #self.panel.show()
        #self.window.clear()
        selection = None

        while True:
            self.view.show()

            #key = self.window.getch()
            logger.info(self.__class__.__name__ + " waiting for input")
            key = self.input.pop()
            logger.info(self.__class__.__name__ + " input is " + key.getKey())

            if key.isKey('CMD_QUIT'):
              selection = MenuSelection('CMD_QUIT')
              break

            elif key.isKey('KEY_LEFT'):
              break

            elif key.isKey('KEY_ENTER') or key.isKey('KEY_RIGHT'):
                item = self.view.getCurrentSelection()
                if item == None:
                  break
                if isinstance(item[1], Menu):
                  selection = item[1].display()
                  if selection is not None:
                    selection.pushContext(item[0])
                    break
                elif callable(item[1]):
                  item[1]()                           
                else:
                  selection = MenuSelection(item[1])
                  if selection is not None:
                    selection.pushContext(item[0])
                  break
                  #start child process

            elif self.view.parseKey(key):
              pass

        self.view.hide()
        return selection

