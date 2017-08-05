import evdev
import sys
from configreader import CONFIG

CONFIG_SECTION = 'input'
CONFIG_DEVPATH = 'devicepath'
CONFIG_DEVNAME = 'devicename'
CONFIG_DEVPHYS = 'devicephys'

class RemoteControl:
  def __init__(self, keydispatcher):
    self.keydispatcher = keydispatcher
    if CONFIG.get(CONFIG_SECTION, 'devicepath') is None:
      self.setup()

  def setup(self):
    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    if len(devices) == 0:
      return None
    print("Please chose an Input Device")
    while True:
      i = 1
      for device in devices:
        print(i, device.fn, device.name, device.phys)
        i += 1
      print("Enter the device number: ")
      try:
        n = sys.stdin.readline()
        n = int(n)
      except:
        n = 0
      i = 1
      for device in devices:
        if i==n:
          CONFIG.set(CONFIG_SECTION, CONFIG_DEVPATH, device.fn)
          CONFIG.set(CONFIG_SECTION, CONFIG_DEVNAME, device.name)
          CONFIG.set(CONFIG_SECTION, CONFIG_DEVPHYS, device.phys)
          return
        i += 1
      print("Invalid device number " + str(n) + ", please try again")
    
  def readLoop(self):
    device = evdev.InputDevice(CONFIG.get(CONFIG_SECTION, CONFIG_DEVPATH))
    print("Opening device:", device)
    device.grab()
    for event in device.read_loop():
      if event.type == evdev.ecodes.EV_KEY:
        keyevent = evdev.KeyEvent(event)
        if keyevent.keystate in (1, 2): #state: 0=up, 1=down, 2=hold
          keycode = keyevent.keycode
          self.keydispatcher.dispatch(keycode)
          print("scancode: ", evdev.KeyEvent(event).scancode, "keycode:", evdev.KeyEvent(event).keycode)
          #print("event:", evdev.categorize(event))

