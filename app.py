import curses
import signal, sys
import time

import inputbuffer 
import mainthread
from logger import logger
import remotecontrol
import keymap
import keydispatcher




def signal_handler(signal, frame):
  logger.info('You pressed Ctrl+C!')
  #print('You pressed Ctrl+C!')
  _keydispatcher.dispatch('CMD_QUIT')
  rc.close()



class FKeyDispatcher:
  def __init__(self, input):
    self.input = input

  def dispatch(self, event):
    logger.info(self.__class__.__name__ + '.dispatch(): ' + event.getKey())
    #print(self.__class__.__name__, event.getKey(), event.getValue())
    time.sleep(1)


class App:
  def __init__(self, stdscreen):
    global mainthread
    global _keydispatcher
    global rc
    logger.info('started')
    input = inputbuffer.InputBuffer()
    fdispatcher = FKeyDispatcher(input)
    _keymap = keymap.KeyMap()
    _keydispatcher = keydispatcher.KeyDispatcher(_keymap)
    _keydispatcher.register_default_listener(input)
    _keydispatcher.register_key_listener('KEY_1', fdispatcher)
    _keydispatcher.register_key_listener('KEY_Q', fdispatcher)
    rc = remotecontrol.RemoteControl(_keydispatcher)
    mainthread = mainthread.MainThread(input,stdscreen)
    mainthread.start()

    logger.info('rc.loop')
    rc.readLoop()
  



if __name__ == '__main__':
  signal.signal(signal.SIGINT,signal_handler)
  curses.wrapper(App)

