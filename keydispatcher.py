import keyevent
from logger import logger

class KeyDispatcher:
  def __init__(self, keymap):
    self.key_listeners = {}
    self.default_listeners = []
    self.keymap = keymap

  def register_key_listener(self, key, listener):
    self.key_listeners[key] = listener

  def register_default_listener(self, listener):
    self.default_listeners.append(listener)

  def dispatch(self, key):
    logger.info(self.__class__.__name__ + " dispatching key: " + key)
    value = self.keymap.map(key)
    event = keyevent.KeyEvent(key, value)
    if value is not None and key in self.key_listeners:
      self.key_listeners[key].dispatch(event)
      return
    for listener in self.default_listeners:
      listener.dispatch(event)


