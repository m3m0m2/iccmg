import keyevent
from logger import logger

class KeyDispatcher:
  def __init__(self, keymap, customkeymap):
    self.key_listeners = {}
    self.default_listeners = []
    self.keymap = keymap
    self.customkeymap = customkeymap

  def register_key_listener(self, key, listener):
    self.key_listeners[key] = listener

  def register_default_listener(self, listener):
    self.default_listeners.append(listener)

  def dispatch(self, key):
    if self.customkeymap is not None and key in self.customkeymap:
      key = self.customkeymap[key]
    value = self.keymap.map(key)
    #if value == None:
    #  value = key
    logger.info(self.__class__.__name__ + " dispatching key: " + str(key) + ", value: '" + repr(value) + "'")
    event = keyevent.KeyEvent(key, value)
    if value is not None and key in self.key_listeners:
      self.key_listeners[key].dispatch(event)
      return
    for listener in self.default_listeners:
      if listener.hasActiveInput():
        listener.dispatch(event)
        return


