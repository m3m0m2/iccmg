import sys
import logging


def setLogger(name=None, filename=None):
  global logger
  if name is None:
    name = sys.argv[0]
  if filename is None:
    filename = name + '.log'
  logger = logging.getLogger(name)
  handler = logging.FileHandler(filename)
  formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler) 
  logger.setLevel(logging.INFO)

  
setLogger()
