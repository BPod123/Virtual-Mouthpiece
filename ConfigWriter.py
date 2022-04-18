"""
Author: Ben Podrazhansky
This file is used for generating configuration files
"""
import json
import os.path

from Manager import ConfigProps
import socket
import argparse

default_props = {
        ConfigProps.SERVER_ADDR.value: socket.gethostbyname(socket.gethostname()),
        ConfigProps.SERVER_PORT.value: 9001,
        ConfigProps.HOST_PORT.value: 9010,
        ConfigProps.NAME.value: "Billboard 9002",
        ConfigProps.HEIGHT.value: None,
        ConfigProps.WIDTH.value: None,
    ConfigProps.TRANSITION_DURATION.value: 1.5,
    }

help = {
  ConfigProps.SERVER_ADDR.value: f"Input type {type(socket.gethostbyname(socket.gethostname()))} ip address",
  ConfigProps.SERVER_PORT.value: f"Input type {type(9001)} port number",
  ConfigProps.HOST_PORT.value: f"Input type {type(9002)} port number",
  ConfigProps.NAME.value: f"Input type {type('Billboard 9002')}",
  ConfigProps.HEIGHT.value: f"Input type {type(500)} pixels",
  ConfigProps.WIDTH.value: f"Input type {type(700)} pixels",
  ConfigProps.TRANSITION_DURATION.value: f"Input type {type(1.5)} seconds",
  "DEST": "Path to save the config file to"
}
parser = argparse.ArgumentParser()
[parser.add_argument(f"-{key}", help=f"Input a {help[key]}") for key in help]


def WriteConfig(dest: str, SERVER_ADDR=None, SERVER_PORT=None, HOST_PORT=None, NAME=None, HEIGHT=None, WIDTH=None, TRANSITION_DURATION=None):
    """
    :param dest: string: Path to where to store the file
    :param SERVER_ADDR: string: IP address
    :param SERVER_PORT: int: Port number of server
    :param HOST_PORT: int: Port number that display computer will host on
    :param NAME: string: Name of display
    :param HEIGHT: int: Height in pixels
    :param WIDTH: int: Width in pixels
    :param TRANSITION_DURATION: float: Number of seconds to allow for transition.
    """
    props = {
        ConfigProps.SERVER_ADDR.value: type(default_props[ConfigProps.SERVER_ADDR.value])(SERVER_ADDR) if SERVER_ADDR is not None else default_props[ConfigProps.SERVER_ADDR.value],
        ConfigProps.SERVER_PORT.value: type(default_props[ConfigProps.SERVER_PORT.value])(SERVER_PORT) if SERVER_PORT is not None else default_props[ConfigProps.SERVER_PORT.value],
        ConfigProps.HOST_PORT.value: type(default_props[ConfigProps.HOST_PORT.value])(HOST_PORT) if HOST_PORT is not None else default_props[ConfigProps.HOST_PORT.value],
        ConfigProps.NAME.value: type(default_props[ConfigProps.NAME.value])(NAME) if NAME is not None else default_props[ConfigProps.NAME.value],
        ConfigProps.HEIGHT.value: type(default_props[ConfigProps.HEIGHT.value])(HEIGHT) if HEIGHT is not None else default_props[ConfigProps.HEIGHT.value],
        ConfigProps.WIDTH.value: type(default_props[ConfigProps.WIDTH.value])(WIDTH) if WIDTH is not None else default_props[ConfigProps.WIDTH.value],
        ConfigProps.TRANSITION_DURATION.value: type(default_props[ConfigProps.TRANSITION_DURATION.value])(TRANSITION_DURATION) if TRANSITION_DURATION is not None else default_props[ConfigProps.TRANSITION_DURATION.value],
    }
    with open(dest, "w") as f:
        json.dump(props, f, indent=4)
def getOption(instruction, type, default):
    while True:
        try:
            choice = input(instruction)
            if choice.lower().replace(" ", "") == "auto":
                return default
            else:
                choice = type(choice)
            return choice
        except:
            print("Invalid input. Must be of type {0}, or 'Auto'".format(type))

def createConfigCommandLine(path):
    config = {
        ConfigProps.SERVER_ADDR.value: getOption(f"""Input the server ip address. or 'Auto' to use the default.\n The default setting is {socket.gethostbyname(socket.gethostname())} (This machine).""", str, socket.gethostbyname(socket.gethostname())),
        ConfigProps.SERVER_PORT.value: getOption("""Input the port number that the server is hosting on, or 'Auto' to use the default. The default setting is 9001.""", int, 9001),
        ConfigProps.NAME.value: getOption("""Input the name of this display or 'Auto' to use the default. The default setting is 'Virtual-Mouthpiece'.""", str, "Virtual-Mouthpiece"),
        ConfigProps.HEIGHT.value: getOption("""Input the height of this display in pixels or 'Auto' to use the default. The default setting is use the primary display's height in pixels.""", int, None),
        ConfigProps.WIDTH.value: getOption("""Input the width of this display in pixels or 'Auto' to use the default. The default setting is to use the primary display's width in pixels.""", int, None),
        ConfigProps.HOST_PORT.value: getOption("""Input the port number for the display to use to connect to the server or 'Auto' to use the default. The default setting is 9010.""", int, 9010),
        ConfigProps.TRANSITION_DURATION.value: getOption("""Input the time to use for transitioning between slides in seconds, or 'Auto'. The default setting is 2.""", float, 2),
    }
    with open(path, "w") as f:
        json.dump(config, f, indent=4)


if __name__ == '__main__':
    args = parser.parse_args()
    props = default_props.copy()
    if hasattr(args, "DEST") and args.DEST is not None:
        if os.path.isfile:
            raise Exception(f"File already exists at {args.DEST}")
        if not os.path.exists(args.DEST):
            raise Exception(f"Directory does not exist: {args.DEST[:args.DEST.rfind(os.path.basename(args.DEST))]}")
        savePath = args.DEST
    else:
        savePath = "Config.json"

    for key in props:
        if hasattr(args, key) and getattr(args, key) is not None:
            desiredType = type(default_props[key])
            try:
                props[key] = desiredType(getattr(args, key))
            except:
                isFloat = False
                if desiredType == int:
                    try:
                        number = float(getattr(args, key))
                        isFloat = True
                    except:
                        pass
                if isFloat:
                    exceptionMessage = f"{key} should be type {type(default_props[key])}, not {type(1.32)}"
                else:
                    exceptionMessage = f"{key} should be type {type(default_props[key])}, not {type(getattr(args, key))}"
                raise Exception(exceptionMessage)

    with open(savePath, "w") as f:
        json.dump(props, f, indent=4)