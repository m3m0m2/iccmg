import collections
import time
import threading

class InputBuffer:
  def __init__(self):
    self.clear()

  def clear(self):
    self.buffer = collections.deque()
    self.lock = threading.Lock()
    self.pauser = threading.Event()

  def push(self, key):
    self.waitIfPaused()
    self.lock.acquire()
    self.buffer.append(key)
    self.lock.release()

  def length(self):
    self.waitIfPaused()
    self.lock.acquire()
    l=len(self.buffer)
    self.lock.release()
    return l

  def pop(self):
    obj = None
    self.waitIfPaused()
    self.lock.acquire()
    if len(self.buffer) > 0:
      obj = self.buffer.popleft()
    self.lock.release()
    return obj

  def popWait(self):
    while True:
      obj = None
      if not self.isPaused():
        obj = self.pop()
      if obj == None:
        time.sleep(0.1)
      else:
        return obj


  def waitIfPaused(self):
    while self.isPaused():
      time.sleep(0.1)

  def isPaused(self):
    return self.pauser.is_set()

  def pause(self):
    self.pauser.set()

  def unpause(self):
    self.pauser.clear()

  def dispatch(self, key, value):
    self.push(key)

