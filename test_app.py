import remotecontrol
import keymap
import keydispatcher
import inputbuffer 
import signal, sys
import time,threading
import mainthread


def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  mainthread.stop()
  sys.exit(0)


class FKeyDispatcher:
  def __init__(self, input):
    self.input = input

  def dispatch(self, event):
    print(self.__class__.__name__, event.getKey(), event.getValue())
    time.sleep(1)

"""
class MainThread(threading.Thread):
  def __init__(self,input):
    self.input = input
    super(MainThread, self).__init__()
    self.stopper = threading.Event()

  def stop(self):
    self.stopper.set()

  def isStopped(self):
    return self.stopper.is_set()

  def run(self):
    while True:
      time.sleep(0.1)
      event = self.input.popWait(1)
      #event = self.input.pop()
      if event is not None:
        print("worked input:", event.getKey())
      if self.isStopped():
        break
"""


def test():
  global mainthread
  signal.signal(signal.SIGINT,signal_handler)

  input = inputbuffer.InputBuffer()
  fdispatcher = FKeyDispatcher(input)
  _keymap = keymap.KeyMap()
  _keydispatcher = keydispatcher.KeyDispatcher(_keymap)
  _keydispatcher.register_default_listener(input)
  _keydispatcher.register_key_listener('KEY_1', fdispatcher)
  _keydispatcher.register_key_listener('KEY_Q', fdispatcher)


  rc = remotecontrol.RemoteControl(_keydispatcher)

  mainthread = mainthread.MainThread(input)
  mainthread.start()

  rc.readLoop()
  



test()
