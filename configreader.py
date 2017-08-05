import ConfigParser


class ConfigReader:
  def __init__(self, configfile=r'config.ini'):
    self.configfile = configfile
    self.load()

  def load(self):
    self.config = ConfigParser.RawConfigParser()
    self.config.read(self.configfile)

  def get(self, section, key):
    try:
      return self.config.get(section, key)
    except:
      return None

  def set(self, section, key, value):
    if not self.config.has_section(section):
      self.config.add_section(section)
    self.config.set(section, key, value)
    self.save()

  def save(self):
    with open(self.configfile, 'wb') as file:
      self.config.write(file)


CONFIG = ConfigReader()
