import sys
from files import Files
import childprocess
from configreader import CONFIG
import re
import os

CONFIG_SECTION = 'sat'
CONFIG_PLAYER = 'player'
CONFIG_STOPPER = 'stopper'

class Sat:
  def __init__(self):
    self.proc = childprocess.ChildProcess()
    if CONFIG.get( CONFIG_SECTION, CONFIG_PLAYER) is None:
      self.setup()
    self.player = CONFIG.get( CONFIG_SECTION, CONFIG_PLAYER)
    self.stopper = CONFIG.get( CONFIG_SECTION, CONFIG_STOPPER)

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


  def getMenu(self):
    m = []
    
    channelre = re.compile('.*://\d*@?([^\(]*)')
    try:
      file = open('menu/sat/channels.conf', 'r')
      lines = file.read().splitlines()
      for line in lines:
        match = channelre.match(line)
        if match:
          channel = match.group(1)
          item = ( channel, line )
          m.append( item )
    except:
      pass
    return m
    
  def start(self, stream):
    self.stop()
    cmd = self.player.split()
    cmd.append(stream)
    self.proc.start(cmd, hideoutput=True)

  def stop(self):
    os.system(self.stopper)

  def isRunning(self):
    #TODO: findout if this runs in the background 
    return self.proc.isRunning()
