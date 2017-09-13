from files import Files, SubDir, File
from logger import logger
import childprocess

class Video:
  def __init__(self):
    self.loop = True
    self.mute = True
    self.proc = childprocess.ChildProcess()
    self.files = []

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

  def addFileEntry(self, file):
    pos = len(self.files)
    self.files.append(file)
    return pos

  def createDirEntries(self, subdir):
    entries = []

    for child in subdir.getChildren():
      if isinstance(child, File):
        pos = self.addFileEntry(subdir)
        #item = [ '.', subdir.getPath() ]
        item = [ '.', str(pos) ]
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
        pos = self.addFileEntry(child)
        #item = [ child.getBasename(), child.getPath() ]
        item = [ child.getBasename(), str(pos) ]
        entries.append(item)

    return entries


  def getMenu(self):
    self.files = []
    dir = Files.ls_recursive('menu/media/', ['.avi', '.mov', '.mkv', '.mp4', '.m4v'])
    entries = self.createDirEntries(dir)
    logger.info(self.__class__.__name__ + " menu: " + str(entries))
    return entries
    

  def start(self, i):
    self.stop()
    cmd = [ 'omxplayer']
    if self.mute:
      cmd.extend(['-n', '-1'])
    self.currentChannelId = int(i)
    node=self.files[self.currentChannelId]
    if isinstance(node, File):
      path=node.getPath()
      cmd.append(path)
      self.proc.start(cmd, hideoutput=True)

  def next(self):
    self.currentChannelId += 1
    if self.currentChannelId >= len(self.files) or self.files[self.currentChannelId].getBasename() == '.':
      self.currentChannelId -= 1
    self.start( self.currentChannelId)

  def prev(self):
    self.currentChannelId -= 1
    if self.currentChannelId < 0 or self.files[self.currentChannelId].getBasename() == '.':
      self.currentChannelId += 1
    self.start( self.currentChannelId)

  def stop(self):
    if self.isRunning():
      self.proc.send('q')

  def isRunning(self):
    return self.proc.isRunning()


  def handleInput(self, input):
    while self.isRunning():
      keyevent = input.popWait(0.5)
      if keyevent is None:
        continue
      if keyevent.isKey('KEY_CHANNELUP'):
        self.next()
      elif keyevent.isKey('KEY_CHANNELDOWN'):
        self.prev()
      elif keyevent.isKey('KEY_LEFT'):
        #self.proc.send(keyevent.getValue())
        self.proc.send("\x1B[D")
      elif keyevent.isKey('KEY_RIGHT'):
        #self.proc.send(keyevent.getValue())
        self.proc.send("\x1B[C")
      elif keyevent.isKey('KEY_STOP'):
        self.stop()
        break
      elif keyevent.isKey('CMD_QUIT'):
        self.stop()
        return 'CMD_QUIT'

  
