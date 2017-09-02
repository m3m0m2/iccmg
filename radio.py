import sys
from files import Files
import childprocess
from configreader import CONFIG

CONFIG_SECTION = 'radio'
CONFIG_PLAYAPP = 'playapp'

class Radio:
  def __init__(self):
    self.proc = childprocess.ChildProcess()
    if CONFIG.get( CONFIG_SECTION, CONFIG_PLAYAPP) is None:
      self.setup()
    self.radioapp = CONFIG.get( CONFIG_SECTION, CONFIG_PLAYAPP)

  def setup(self):
    while True:
      i = 1
      options = [ 'mplayer' ]
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
          CONFIG.set(CONFIG_SECTION, CONFIG_PLAYAPP, option)
          return
        i += 1
      print("Invalid option number " + str(n) + ", please try again")


  def getMenu(self):
    m = []
    for f in Files.ls('menu/radio', ['.url']):
      with open(f.getPath(), 'r') as file:
        stream = file.read().replace('\n', '')
      item = ( f.getBasename(), stream )
      m.append( item )
    return m
    
  def start(self, stream):
    self.proc.start([self.radioapp, stream])

  def stop(self):
    self.proc.stop()

  def isRunning(self):
    return self.proc.isRunning()
