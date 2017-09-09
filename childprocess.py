import subprocess
import os
from logger import logger



class ChildProcess:
  def __init__(self):
    self.proc = None
    self.DEVNULL = open(os.devnull, 'w')
    #signal.signal(signal.SIGCHLD, self.handleSIGCHLD)

  def start(self, cmd, hideoutput = False):
    self.stop()
    if type(cmd) is list or type(cmd) is tuple:
      self.cmd = cmd
    else:
      self.cmd = [cmd]

    # setsid creates new session
    if hideoutput:
      logger.info(self.__class__.__name__ + " starting hiding: " + str(self.cmd))
      self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=self.DEVNULL, stderr=self.DEVNULL, preexec_fn=os.setsid)
    else:
      logger.info(self.__class__.__name__ + " starting: " + str(self.cmd))
      self.proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, preexec_fn=os.setsid)

  def dispatch(self, event):
    if event.isKey('CMD_QUIT'):
      self.stop()
    else:
      self.send(event.getValue())

  def hasActiveInput(self):
    return self.isRunning()

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
    try:
      if self.isRunning():
        #os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        logger.info(self.__class__.__name__ + " stopping: " + str(self.cmd))
        self.proc.terminate()
        self.proc.wait(2)
    except:
      pass
