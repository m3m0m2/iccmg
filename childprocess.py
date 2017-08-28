from subprocess import Popen, PIPE, STDOUT
import os
from logger import logger



class ChildProcess:
  def __init__(self):
    self.proc = None
    #signal.signal(signal.SIGCHLD, self.handleSIGCHLD)

  def start(self, cmd):
    self.stop()
    self.cmd = cmd
    logger.info(self.__class__.__name__ + " starting: " + str(self.cmd))
    #self.proc = Popen([self.cmd], stdin=PIPE, preexec_fn=os.setsid) #setsid creates new session
    self.proc = Popen([self.cmd], stdin=PIPE)

  def dispatch(self, event):
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
      except subprocess.TimeoutExpired:
        pass
