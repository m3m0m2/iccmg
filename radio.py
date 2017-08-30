from files import Files

class Radio:
  def __init__(self):
    pass

  def getMenu(self):
    m = []
    for f in Files.ls('menu/radio', ['.url']):
      item = ( f.getBasename(), f.getPath() )
      m.append( item )
    return m
    
