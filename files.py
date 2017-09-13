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
    return os.path.splitext(self.path)[1].lower()

  def isExecutable(self):
    return os.access(self.path, os.X_OK)
  
class SubDir:
  def __init__(self, path):
    self.path = path 
    self.children = []

  def getPath(self):
    return self.path

  def getName(self):
    return os.path.splitext(os.path.basename(self.path))[0]

  def getChildren(self):
    return self.children

  def addChild(self, child):
    return self.children.append(child)
    



class Files:
  @staticmethod
  def ls(dir, extensions = [], onlyExecutable = False):
    files = [File(os.path.join(dir, f)) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    if len(extensions) > 0:
      files = [f for f in files if f.getExtension() in extensions]
    if onlyExecutable:
      files = [f for f in files if f.isExecutable() ]
    return files

  @staticmethod
  def ls_recursive(dir, extensions = [], onlyExecutable = False):
    sdirs = {}
    sdirs[dir] = SubDir(dir)
    for root, dirs, files in os.walk(dir, followlinks=True):
      dirs.sort()
      files.sort()

      for d in dirs:
        path = os.path.join(root, d)
        sdirs[path] = SubDir(path)
        sdirs[root].addChild(sdirs[path])
        
      for name in files:
        path = os.path.join(root, name)
        f = File(path)
        if len(extensions) == 0 or f.getExtension() in extensions:
          sdirs[root].addChild(f)
        
    return sdirs[dir]





