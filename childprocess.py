from subprocess import Popen, PIPE, STDOUT
import os




class ChildProcess:
  def __init__(self):
    self.proc = None
    #signal.signal(signal.SIGCHLD, self.handleSIGCHLD)

  def start(self, cmd):
    self.stop()
    self.cmd = cmd
    self.proc = Popen([self.cmd], stdin=PIPE, preexec_fn=os.setsid)

  def dispatch(self, event):
    self.send(event.getValue())

  def send(self, msg):
    if self.isRunning():
      try:
        self.proc.stdin.write(msg)
        self.proc.stdin.flush()
      except:
        pass

  def isRunning(self):
    if self.proc is None:
      return False
    return self.proc.poll() == None

  def stop(self):
    if self.isRunning():
      #os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
      self.proc.terminate()
      try:
        self.proc.wait(5)
      except subprocess.TimeoutExpired:
        pass
