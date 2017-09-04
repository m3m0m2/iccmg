import curses                                                                
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


class Menu(object):                                                          

    def __init__(self, input, items, stdscreen, levely, levelx):                                    
        self.input = input
        [ rows, cols ] = self.menuSize(items)
        self.window = stdscreen.subwin(rows + 2,cols + 5,levely,levelx)                                  
        self.window.keypad(1)                                                
        self.panel = panel.new_panel(self.window)                            
        self.panel.hide()                                                    
        panel.update_panels()                                                

        self.position = 0                                                    
        self.items = items 
        for i in range(len(self.items)):
          item = self.items[i]
          if type(item[1]) is list:
            submenu = Menu(self.input, item[1], stdscreen, levely + i, levelx + 5 + cols)
            self.items[i] = (item[0], submenu)
       
        #self.items.append(('exit','exit'))                                   

    def menuSize(self, items):
      maxlen=0
      curlen=0
      for item in items:
        curlen=len(item[0])
        if len(item) > 2:
          curlen += 4
        if curlen > maxlen:
          maxlen = curlen
      return [len(items), maxlen]


    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()
        selection = None

        while True:
            self.window.box()                                            
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   
                if len(item) > 2:
                  msg = '%d. %s [%s]' % (index, item[0], 'X' if item[2]() else ' ')
                else:
                  msg = '%d. %s' % (index, item[0])
                self.window.addstr(1+index, 1, msg, mode)
            self.window.refresh()                                            
            curses.doupdate()                                                

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
                if isinstance(self.items[self.position][1], Menu):
                  selection = self.items[self.position][1].display()
                  if selection is not None:
                    selection.pushContext(self.items[self.position][0])
                    break
                elif callable(self.items[self.position][1]):
                  self.items[self.position][1]()                           
                else:
                  selection = MenuSelection(self.items[self.position][1])
                  if selection is not None:
                    selection.pushContext(self.items[self.position][0])
                  break
                  #start child process

            elif key.isKey('KEY_UP'): 
                self.navigate(-1)                                            

            elif key.isKey('KEY_DOWN'):
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()
        return selection

