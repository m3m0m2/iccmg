from files import Files, SubDir, File
from logger import logger
import childprocess

class Video:
  def __init__(self):
    self.loop = True
    self.mute = True
    self.proc = childprocess.ChildProcess()

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

  def getSettingsMenu(self):
    return [
            ('Loop', self.toggleLoop, self.getLoop),
            ('Mute', self.toggleMute, self.getMute)
           ]

  def createDirEntries(self, subdir):
    entries = []

    for child in subdir.getChildren():
      if isinstance(child, File):
        item = [ '.', subdir.getPath() ]
        entries.append(item)
        break

    for child in subdir.getChildren():
      item = []
      if isinstance(child, SubDir):
        subentries = self.createDirEntries(child) 
        if len(subentries) > 0:
          item = [ child.getName(), subentries ]
          entries.append(item)
      elif isinstance(child, File):
        item = [ child.getBasename(), child.getPath() ]
        entries.append(item)

    return entries


  def getMenu(self):
    dir = Files.ls_recursive('menu/media/', ['.avi', '.mov', '.mkv', '.mp4', '.m4v'])
    entries = self.createDirEntries(dir)
    logger.info(self.__class__.__name__ + " menu: " + str(entries))
    return entries
    

  def start(self, path):
    cmd = [ 'omxplayer']
    if self.mute:
      cmd.extend(['-n', '-1'])
    cmd.append(path)
    self.proc.start(cmd, hideoutput=True)

  def stop(self):
    self.proc.stop()

  def isRunning(self):
    return self.proc.isRunning()


  def handleInput(self, input):
    while self.isRunning():
      keyevent = input.popWait(0.5)
      if keyevent is None:
        continue
      #if keyevent.isKey('KEY_CHANNELUP'):
      #  self.next()
      #elif keyevent.isKey('KEY_CHANNELDOWN'):
      #  self.prev()
      elif keyevent.isKey('KEY_STOP'):
        self.stop()
        break
      elif keyevent.isKey('CMD_QUIT'):
        self.stop()
        return 'CMD_QUIT'

  
