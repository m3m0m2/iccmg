import sys, os
from files import Files
import childprocess
from configreader import CONFIG


class Game:
  def __init__(self):
    self.proc = childprocess.ChildProcess()
    self.games = []

  def which(self,program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


  def updateMenu(self):
    self.games = []
    conf = 'menu/games/games.conf'
    try:
      with open(conf) as f:
        lines = [line.rstrip('\r\n') for line in f]
        for line in lines:
          item = line.split('\t')
          if len(item) != 2:
            continue
          args = item[1].split(' ')
          app = self.which(args[0])
          args[0] = app
          if app == None:
            continue
          item[1] = ' '.join(args)
          self.games.append(item)
    except:
      pass


  def getMenu(self):
    self.updateMenu()
    return self.games


    
  def start(self, cmdstr):
    self.stop()
    cmd = cmdstr.split(' ')
    cmd[0] = self.which(cmd[0])
    self.proc.start(cmd, hideoutput=False)

  def stop(self):
    self.proc.stop()

  def isRunning(self):
    return self.proc.isRunning()

