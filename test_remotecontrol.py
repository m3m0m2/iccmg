import remotecontrol
import keymap
import keydispatcher
import signal, sys

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  sys.exit(0)


class DispatcherA:
  def __init__(self):
    pass

  def dispatch(self, key, value):
    print(self.__class__.__name__, key, value)


class DispatcherB:
  def __init__(self):
    pass

  def dispatch(self, key, value):
    print(self.__class__.__name__, key, value)


def test1():
  signal.signal(signal.SIGINT,signal_handler)

  dispatcherA = DispatcherA()
  dispatcherB = DispatcherB()
  _keymap = keymap.KeyMap()
  _keydispatcher = keydispatcher.KeyDispatcher(_keymap)
  _keydispatcher.register_default_listener(dispatcherA)
  _keydispatcher.register_key_listener('KEY_1', dispatcherB)
  _keydispatcher.register_key_listener('KEY_2', dispatcherB)
  _keydispatcher.register_key_listener('KEY_3', dispatcherB)


  rc = remotecontrol.RemoteControl(_keydispatcher)
  rc.readLoop()



test1()
