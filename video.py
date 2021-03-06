from files import Files, SubDir, File
from logger import logger
import childprocess

class Video:
  def __init__(self):
    self.loop = True
    self.mute = True
    self.proc = childprocess.ChildProcess()
    self.files = []
    self.modedir = False

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

  #order: ., current dir files, subdirs
  def createDirEntries(self, subdir):
    entries = []

    for child in subdir.getChildren():
      if isinstance(child, File):
        pos = self.addFileEntry(subdir)
        item = [ '.', str(pos) ]
        entries.append(item)
        logger.info(self.__class__.__name__ + " createDirEntries %s type %s" % (str(item), type(self.files[pos])))
        break

    for child in subdir.getChildren():
      item = []
      if isinstance(child, File):
        pos = self.addFileEntry(child)
        item = [ child.getBasename(), str(pos) ]
        entries.append(item)
        logger.info(self.__class__.__name__ + " createDirEntries %s type %s" % (str(item), type(self.files[pos])))

    for child in subdir.getChildren():
      item = []
      if isinstance(child, SubDir):
        subentries = self.createDirEntries(child) 
        if len(subentries) > 0:
          item = [ child.getName(), subentries ]
          entries.append(item)

    return entries


  def getMenu(self):
    self.files = []
    dir = Files.ls_recursive('menu/media/', ['.avi', '.mov', '.mkv', '.mp4', '.m4v'])
    entries = self.createDirEntries(dir)
    logger.info(self.__class__.__name__ + " menu: " + str(entries))
    return entries
    
  def play(self):
    self.stop()
    cmd = [ 'omxplayer']
    if self.mute:
      cmd.extend(['-n', '-1'])
    node=self.files[self.currentChannelId]
    if isinstance(node, File):
      path=node.getPath()
      cmd.append(path)
      self.proc.start(cmd, hideoutput=True)
    

  def start(self, i):
    self.currentChannelId = int(i)
    node=self.files[self.currentChannelId]
    if isinstance(node, SubDir):
      self.modedir = True
      self.next()
    else:
      self.modedir = False
    self.play()


  def next(self):
    logstatus = [ self.currentChannelId ]
     
    self.currentChannelId += 1
    if self.currentChannelId >= len(self.files) or isinstance(self.files[self.currentChannelId], SubDir):
      self.currentChannelId -= 1
      logger.info(self.__class__.__name__ + " next(%d -> %d) " % (logstatus[0], logstatus[0]))
      return False
    logstatus.append( self.currentChannelId )
    logger.info(self.__class__.__name__ + " next(%d -> %d) " % (logstatus[0], logstatus[1]))
    return True

  def prev(self):
    logstatus = [ self.currentChannelId ]

    self.currentChannelId -= 1
    if self.currentChannelId < 0 or isinstance(self.files[self.currentChannelId], SubDir):
      self.currentChannelId += 1
      logger.info(self.__class__.__name__ + " prev(%d -> %d) " % (logstatus[0], logstatus[0]))
      return False
    logstatus.append( self.currentChannelId )
    logger.info(self.__class__.__name__ + " prev(%d -> %d) " % (logstatus[0], logstatus[1]))
    return True

  def rewindFirst(self):
    logstatus = [ self.currentChannelId ]
    while self.prev():
      pass
    logstatus.append( self.currentChannelId )
    logger.info(self.__class__.__name__ + " rewindFirst(%d -> %d) " % (logstatus[0], logstatus[1]))

  def rewindLast(self):
    logstatus = [ self.currentChannelId ]
    while self.next():
      pass
    logstatus.append( self.currentChannelId )
    logger.info(self.__class__.__name__ + " rewindLast(%d -> %d) " % (logstatus[0], logstatus[1]))

  def stop(self):
    if self.isRunning():
      self.proc.send('q')

  def isRunning(self):
    return self.proc.isRunning()


  def handleInput(self, input):
    while True:
      running = self.isRunning()
      if not running:
        if self.modedir:
          if self.next():
            self.play()
          elif self.getLoop():
            self.rewindFirst()
            self.play()
          else:
            break
        elif self.getLoop():
          self.play()
        else:
          break

      keyevent = input.popWait(0.5)
      if keyevent is None:
        continue
      if keyevent.isKey('KEY_CHANNELUP'):
        if self.next():
          self.play()
        elif self.modedir:
          self.rewindFirst()
          self.play()
      elif keyevent.isKey('KEY_CHANNELDOWN'):
        if self.prev():
          self.play()
        elif self.modedir:
          self.rewindLast()
          self.play()
      elif keyevent.isKey('KEY_LEFT'):
        #self.proc.send(keyevent.getValue())
        self.proc.send("\x1B[D")
      elif keyevent.isKey('KEY_RIGHT'):
        #self.proc.send(keyevent.getValue())
        self.proc.send("\x1B[C")
      elif keyevent.isKey('KEY_PLAY'):
        self.proc.send(" ")
      elif keyevent.isKey('KEY_STOP'):
        self.stop()
        break
      elif keyevent.isKey('CMD_QUIT'):
        self.stop()
        return 'CMD_QUIT'

  
