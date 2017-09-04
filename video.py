

class Video:
  def __init__(self):
    self.loop = True
    self.mute = True

  def getLoop(self):
    return self.loop

  def getMute(self):
    return self.mute
  
  def toggleLoop(self):
    self.loop = not self.loop
    return self.loop

  def toggleMute(self):
    self.mute = not self.mute
    return self.mute

  def getMenu(self):
    return [
            ('Loop', self.toggleLoop, self.getLoop),
            ('Mute', self.toggleMute, self.getMute)
           ]

