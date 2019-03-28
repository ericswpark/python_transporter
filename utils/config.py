from configparser import SafeConfigParser

config = SafeConfigParser()

def writeConfig(section, key, value):
    config.read('config.ini')
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)

    with open('config.ini', 'w') as config_file:
        config.write(config_file)

def readConfig(section, key):
    config.read('config.ini')
    return config.get(section, key)