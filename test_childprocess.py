import childprocess
import sys
import logging
import time

logger = logging.getLogger('test_childprocess')
handler = logging.FileHandler('test_childprocess.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) 
logger.setLevel(logging.INFO)

logger.info('Start')

proc = childprocess.ChildProcess()
proc.start('bastet')

logger.info('Ran bastet')

while True:
  time.sleep(0.1)
  logger.info('reading')
  line = sys.stdin.read(1)
  logger.info('read ' + line)
  if not line:
    break
  if proc.isRunning():
    proc.send(line)
  else:
    break
  




