
class KeyEvent:
  def __init__(self, key, value):
    self.key = key
    self.value = value

  def getKey(self):
    return self.key

  def getValue(self):
    return self.value

  def isKey(self, key):
    return self.key == key 

