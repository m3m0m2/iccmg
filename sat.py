import sys
from files import Files
import childprocess
from configreader import CONFIG
import re
import os

CONFIG_SECTION = 'sat'
CONFIG_PLAYER = 'player'

class SatChannel:
  def __init__(self, dvburl):
    self.dvburl = dvburl

  def getUrl(self):
    return self.dvburl

  def getName(self):
    channelre = re.compile('.*://\d*@?([^\(]*)')
    match = channelre.match(self.dvburl)
    channel = ''
    if match:
      channel = match.group(1)
    return channel
    

class Sat:
  def __init__(self):
    self.proc = childprocess.ChildProcess()
    if CONFIG.get( CONFIG_SECTION, CONFIG_PLAYER) is None:
      self.setup()
    self.player = CONFIG.get( CONFIG_SECTION, CONFIG_PLAYER)
    self.channels = []
    self.currentChannelId = -1

  def setup(self):
    while True:
      i = 1
      options = [ 'sudo openvt -f -s -c 1 -- sudo -u pi mplayer --really-quiet --hardframedrop -vo sdl' ]
      for option in options:
        print(i, option)
        i += 1
      print("Please setup the Player app: ")
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
    channelre = re.compile('.*://\d*@?([^\(]*)')
    try:
      file = open('menu/sat/channels.conf', 'r')
      lines = file.read().splitlines()
      for line in lines:
        match = channelre.match(line)
        if match:
          newchannel = SatChannel(line)
          self.channels.append(newchannel)
    except:
      pass

  def getMenu(self):
    self.updateChannels()

    m = []
    for i in range(len(self.channels)):
      channel = self.channels[i]
      name = channel.getName()
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
      elif keyevent.isKey('CMD_QUIT'):
        self.stop()
        return 'CMD_QUIT'

    
  def start(self, i):
    self.currentChannelId = int(i)
    self.stop()
    url = self.channels[self.currentChannelId].getUrl()
    cmd = self.player.split()
    cmd.append(url)
    self.proc.start(cmd, hideoutput=True)

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
      
  def stop(self):
    if self.proc.isRunning():
      self.proc.send('q')

  def isRunning(self):
    ret = os.system('pgrep mplayer >/dev/null')
    return True if ret==0 else False
