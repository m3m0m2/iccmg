import sys
from files import Files
import childprocess
from configreader import CONFIG

CONFIG_SECTION = 'radio'
CONFIG_PLAYER = 'player'

class Radio:
  def __init__(self):
    self.proc = childprocess.ChildProcess()
    if CONFIG.get( CONFIG_SECTION, CONFIG_PLAYER) is None:
      self.setup()
    self.radioapp = CONFIG.get( CONFIG_SECTION, CONFIG_PLAYER)
    self.channels = []
    self.currentChannelId = -1

  def setup(self):
    while True:
      i = 1
      options = [ 'mplayer --really-quiet' ]
      for option in options:
        print(i, option)
        i += 1
      print("Please setup the Radio Player app: ")
      try:
        n = sys.stdin.readline()
        n = int(n)
      except:
        n = 0
      i = 1
      for option in options:
        if i==n:
          CONFIG.set(CONFIG_SECTION, CONFIG_PLAYER, option)
          return
        i += 1
      print("Invalid option number " + str(n) + ", please try again")

  def updateChannels(self):
    self.channels = []
    for f in Files.ls('menu/radio', ['.url']):
      with open(f.getPath(), 'r') as file:
        stream = file.read().replace('\n', '')
        item = (f.getBasename(), stream)
      self.channels.append(item)


  def getMenu(self):
    self.updateChannels()

    m = []
    for i in range(len(self.channels)):
      channel = self.channels[i]
      name = channel[0]
      item = ( name, str(i) )
      m.append( item )
    return m

  def handleInput(self, input):
    while self.isRunning():
      keyevent = input.popWait(0.5)
      if keyevent is None:
        continue
      if keyevent.isKey('KEY_CHANNELUP'):
        self.next()
      elif keyevent.isKey('KEY_CHANNELDOWN'):
        self.prev()
      elif keyevent.isKey('KEY_STOP'):
        self.stop()
        break

    
  def start(self, i):
    self.currentChannelId = int(i)
    self.stop()
    url = self.channels[self.currentChannelId][1]
    cmd = self.radioapp.split()
    cmd.append(url)
    self.proc.start(cmd, hideoutput=True)

  def stop(self):
    self.proc.stop()

  def isRunning(self):
    return self.proc.isRunning()

  def next(self):
    self.currentChannelId += 1
    if self.currentChannelId >= len(self.channels):
      self.currentChannelId = len(self.channels) - 1
    self.start(self.currentChannelId)

  def prev(self):
    self.currentChannelId -= 1
    if self.currentChannelId < 0:
      self.currentChannelId = 0
    self.start(self.currentChannelId)

