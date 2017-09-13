import remotecontrol
import keymap
import keydispatcher
import signal, sys
import customkeymap

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  sys.exit(0)


class DispatcherA:
  def __init__(self):
    pass

  def dispatch(self, event):
    print(self.__class__.__name__, event.getKey(), event.getValue())

  def hasActiveInput(self):
    return True


class DispatcherB:
  def __init__(self):
    pass

  def dispatch(self, event):
    print(self.__class__.__name__, event.getKey(), event.getValue())


def test1():
  signal.signal(signal.SIGINT,signal_handler)

  dispatcherA = DispatcherA()
  dispatcherB = DispatcherB()
  _keymap = keymap.KeyMap()
  _customkeymap = customkeymap.keymap_remote
  _keydispatcher = keydispatcher.KeyDispatcher(_keymap, _customkeymap)
  _keydispatcher.register_default_listener(dispatcherA)
  _keydispatcher.register_key_listener('KEY_1', dispatcherB)
  _keydispatcher.register_key_listener('KEY_2', dispatcherB)
  _keydispatcher.register_key_listener('KEY_3', dispatcherB)


  rc = remotecontrol.RemoteControl(_keydispatcher)
  rc.readLoop()



test1()
