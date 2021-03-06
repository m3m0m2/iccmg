import Queue

class InputBuffer:
  def __init__(self):
    self.clear()
    self.active = False

  def clear(self):
    self.queue = Queue.Queue()

  def push(self, event):
    self.queue.put(event)

  def length(self):
    return self.queue.qsize()

  def pop(self):
    obj = self.queue.get()
    self.queue.task_done()
    return obj

  def popWait(self, timeout = 1):
    obj = None
    try:
      obj = self.queue.get(True, timeout)
      self.queue.task_done()
    except:
      obj = None
    return obj

  def hasActiveInput(self):
    return self.active

  def setActiveInput(self, value):
    self.active = value


  def dispatch(self, event):
    self.push(event)

