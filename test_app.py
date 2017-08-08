import remotecontrol
import keymap
import keydispatcher
import inputbuffer 
import signal, sys
import time,threading


def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  mainthread.stop()
  sys.exit(0)


class FKeyDispatcher:
  def __init__(self, input):
    self.input = input

  def dispatch(self, key, value):
    self.input.pause()
    print(self.__class__.__name__, key, value)
    time.sleep(1)
    self.input.unpause()


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
      time.sleep(0.2)
      key = self.input.pop()
      if key is not None:
        print("worked input:", key)
      if self.isStopped():
        break


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

  mainthread = MainThread(input)
  mainthread.start()

  rc.readLoop()
  



test()
