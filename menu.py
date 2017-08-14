import curses                                                                
from curses import panel                                                     

class MenuSelection:
  def __init__(self, cmd):
    self.cmd = cmd

  def getCmd(self):
    return self.cmd


class Menu(object):                                                          

    def __init__(self, items, stdscreen, levely, levelx):                                    
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
            submenu = Menu(item[1], stdscreen, levely + i, levelx + 5 + cols)
            self.items[i] = (item[0], submenu)
       
        #self.items.append(('exit','exit'))                                   

    def menuSize(self, items):
      maxlen=0
      for item in items:
        if len(item[0]) > maxlen:
          maxlen = len(item[0])
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
            self.window.refresh()                                            
            curses.doupdate()                                                
            for index, item in enumerate(self.items):                        
                if index == self.position:                                   
                    mode = curses.A_REVERSE                                  
                else:                                                        
                    mode = curses.A_NORMAL                                   

                msg = '%d. %s' % (index, item[0])                            
                self.window.addstr(1+index, 1, msg, mode)                    

            key = self.window.getch()                                        

            if key == curses.KEY_LEFT:
                    break                                                    
            if key in [curses.KEY_ENTER, ord('\n'),curses.KEY_RIGHT]:                         
                if isinstance(self.items[self.position][1], Menu):
                  selection = self.items[self.position][1].display()                           
                  break
                elif callable(self.items[self.position][1]):
                  self.items[self.position][1]()                           
                else:
                  selection = MenuSelection(self.items[self.position][1])
                  break
                  #start child process

            elif key == curses.KEY_UP:                                       
                self.navigate(-1)                                            

            elif key == curses.KEY_DOWN:                                     
                self.navigate(1)                                             

        self.window.clear()                                                  
        self.panel.hide()                                                    
        panel.update_panels()                                                
        curses.doupdate()
        return selection

class MyApp(object):                                                         

    def __init__(self, stdscreen):                                           
        self.screen = stdscreen                                              
        curses.curs_set(0)                                                   
        
        menu_items = [
                ('Games', [
                           ('Tetris', curses.beep),
                           ('Tetris', 'bastet'),
                           ('Snake', curses.flash)
                          ]),
                ('TV', curses.beep),
                ('Radio', curses.beep)
                ]

        main_menu = Menu(menu_items, self.screen, 0, 0)                       
        main_menu.display()                                                  

if __name__ == '__main__':                                                       
    curses.wrapper(MyApp)   
