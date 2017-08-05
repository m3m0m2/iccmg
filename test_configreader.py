import configreader




conf = configreader.ConfigReader()
value = conf.get('main', 'color')
print(value)
if value is None:
  conf.set('main', 'color', 'red')


