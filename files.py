import os
import os.path


class File:
  def __init__(self, path):
    self.path = path

  def getPath(self):
    return self.path

  def getBasename(self):
    return os.path.splitext(os.path.basename(self.path))[0]

  def getExtension(self):
    return os.path.splitext(self.path)[1]

  def isExecutable(self):
    return os.access(self.path, os.X_OK)
  

class Files:
  @staticmethod
  def ls(dir, extensions = [], onlyExecutable = False):
    files = [File(os.path.join(dir, f)) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    if len(extensions) > 0:
      files = [f for f in files if f.getExtension() in extensions]
    if onlyExecutable:
      files = [f for f in files if f.isExecutable() ]
    return files

