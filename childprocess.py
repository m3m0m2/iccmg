import subprocess
import os
from logger import logger



class ChildProcess:
  def __init__(self):
    self.proc = None
    #signal.signal(signal.SIGCHLD, self.handleSIGCHLD)

  def start(self, cmd):
    self.stop()
    if type(cmd) is list or type(cmd) is tuple:
      self.cmd = cmd
    else:
      self.cmd = [cmd]
    #TODO: if no output option
    # FNULL = open(os.devnull, 'w')
    #subprocess.call(['echo', 'foo'], stdout=FNULL, stderr=subprocess.STDOUT)
    logger.info(self.__class__.__name__ + " starting: " + str(self.cmd))
    self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, preexec_fn=os.setsid) #setsid creates new session

  def dispatch(self, event):
    if event.isKey('CMD_QUIT'):
      self.stop()
    else:
      self.send(event.getValue())

  def send(self, msg):
    logger.info(self.__class__.__name__ + " send('" + msg + "')")
    if self.isRunning():
      try:
        self.proc.stdin.write(msg)
        self.proc.stdin.flush()
        logger.info(self.__class__.__name__ + " sent: '" + msg + "' (len: " + str(len(msg)) + ") to: " + str(self.cmd))
      except:
        pass

  def isRunning(self):
    if self.proc is None:
      return False
    return self.proc.poll() == None

  def stop(self):
    if self.isRunning():
      #os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
      logger.info(self.__class__.__name__ + " stopping: " + str(self.cmd))
      self.proc.terminate()
      try:
        self.proc.wait(5)
      except:
        pass
