import evdev, re

for i in evdev.ecodes.KEY:
  key = evdev.ecodes.KEY[i]
  try:
    value = re.match('^KEY_(.*)$', key).group(1)
  except:
    value = key
  print('  "%s": "%s",' % (key, value))

