#!/usr/bin/python
import curses
import signal, sys
import time

import inputbuffer 
import mainthread
from logger import logger
import remotecontrol
import keymap
import keydispatcher
import childprocess
import customkeymap



def quit():
  _keydispatcher.dispatch('CMD_QUIT')
  rc.close()

def signal_handler(signal, frame):
  logger.info('You pressed Ctrl+C!')
  quit()


class FKeyDispatcher:
  def __init__(self, input):
    self.input = input

  def dispatch(self, event):
    logger.info(self.__class__.__name__ + '.dispatch(): ' + str(event.getKey()))
    if event.isKey('KEY_Q'):
      quit()
    time.sleep(1)


class App:
  def __init__(self, stdscreen):
    global mainthread
    global _keydispatcher
    global rc
    global child
    logger.info('started')
    input = inputbuffer.InputBuffer()
    fdispatcher = FKeyDispatcher(input)
    child = childprocess.ChildProcess()
    _keymap = keymap.KeyMap()
    _customkeymap = customkeymap.keymap_remote
    _keydispatcher = keydispatcher.KeyDispatcher(_keymap, _customkeymap)
    _keydispatcher.register_default_listener(input)
    _keydispatcher.register_default_listener(child)
    _keydispatcher.register_key_listener('KEY_1', fdispatcher)
    _keydispatcher.register_key_listener('KEY_Q', fdispatcher)
    rc = remotecontrol.RemoteControl(_keydispatcher)
    mainthread = mainthread.MainThread(input,stdscreen,child)
    mainthread.start()

    logger.info('rc.loop')
    rc.readLoop()
  



if __name__ == '__main__':
  signal.signal(signal.SIGINT,signal_handler)
  curses.wrapper(App)

