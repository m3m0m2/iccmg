from subprocess import Popen, PIPE, STDOUT



class ChildProcess:
  def __init__(self, cmd):
    self.cmd = cmd
    self.proc = Popen([self.cmd], stdin=PIPE)

  def send(self, msg):
    self.proc.stdin.write(msg)
    self.proc.stdin.flush()

  def isRunning(self):
    return self.proc.poll()

