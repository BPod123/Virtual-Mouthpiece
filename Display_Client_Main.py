from Manager import Manager
import os
import argparse
import ConfigWriter
import json
parser = argparse.ArgumentParser()
parser.add_argument("-Config_Path", help=f"Input a string in the form 'relative/path/to/Config.json' With the settings to run the display on")
def clearConsole():
    try:
        os.system('cls')
    except:
        try:
            os.system('clear')
        except:
            pass
def start(workingDir, configPath):
    manager = Manager(workingDir, configPath)
    manager.start()

if __name__ == '__main__':
    workingDirectory = os.path.abspath("Display Working Directory")
    defaultConfigPath = os.path.join(workingDirectory, "Config.json")
    defaultBackupConfigPath = os.path.join(workingDirectory, "Config_backup.json")
    args = parser.parse_args()
    if args.Config_Path is None:
        print("Config_Path argument not passed in.")
        # No Config Path detected. Check for one
        foundConfigs = []
        for path in [path for path in [os.path.join(workingDirectory, x) for x in os.listdir(workingDirectory)] if os.path.exists(path) and os.path.isfile(path) and path.lower().endswith(".json")]:
            # A config has been found.
            try:
                config = Manager.loadConfig(path)
                if isinstance(config, dict) and False not in [prop.value in config for prop in ConfigWriter.ConfigProps]:
                    foundConfigs.append((path, config))
            except:
                continue
        configPathMap = {}
        if len(foundConfigs) > 0:
            fileListString = '\n'.join([found[0] for found in foundConfigs])
            print(f"Config file{'s' if len(foundConfigs) > 1 else ''} have been detected in \n{fileListString}")
            index = 1
            for path, config in foundConfigs:
                configPathMap[index] = path
                configStr = json.dumps(config).replace("None", "'Auto'")
                print(f"{index}. Config settings for {path}\n{configStr}")
                index += 1
        keys = list(configPathMap)
        keys.sort()
        options = [
            "{0}. Use Config: {1}".format(key, configPathMap[key])
            for key in keys
        ]
        options.append(f"{len(options) + 1}. Create Configuration")
        options.append(f"{len(options) + 1}. Quit")
        while True:
            try:
                choice = int(input("Please select a configuration option.\n{0}\n".format("\n".join(options))).replace(" ", ""))
                if choice in list(range(1, len(options) + 1)):
                    break
            except:
                print("Invalid input. Must be number between {0} and {1}".format(1, len(options)))
        if choice in configPathMap:
            configPath = configPathMap[choice][0]
            start(workingDirectory, configPath)
        elif choice == len(options) - 1:
            # Create config
            configPath = defaultConfigPath
            ConfigWriter.createConfigCommandLine(configPath)
            start(workingDirectory, configPath)
    else:
        # Config file has been passed in
        start(workingDirectory, args.Config_Path)


