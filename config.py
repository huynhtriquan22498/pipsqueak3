"""
config.py - Configuration facilities

Provides fixtures for loading a configuration from disk.

This modules `setup()` function does not need to be called directly, it will be called
    automatically upon first import.

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE
"""
import json
import logging
import os
import coloredlogs
from typing import Union

from Modules import cli_manager  # For CLI config-file argument

config: Union[None, dict] = None


def setup_logging(logfile: str):
    # check for CLI verbosity flag
    if cli_manager.args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # hook the logger
    log = logging.getLogger(f"mecha.{__name__}")

    # create a handler for said logger...
    file_logger = logging.FileHandler(logfile, 'a')
    log_format = '<%(asctime)s %(name)s> [%(levelname)s] %(message)s'
    log_datefmt = '%Y-%m-%d %H:%M:%S'
    file_logger_format = logging.Formatter(log_format)

    # set the formatter to actually use it
    file_logger.setFormatter(file_logger_format)

    # add the handler to the log.
    log.addHandler(file_logger)

    # set proper severity level
    log.setLevel(loglevel)

    # add Console logging
    console = logging.StreamHandler()
    logging.getLogger(f"mecha.{__name__}").addHandler(console)

    # add console logging format
    console_format = logging.Formatter(log_format)

    # set console formatter to use our format.
    console.setFormatter(console_format)

    # coloredlogs hook
    coloredlogs.install(handler=__name__,
                        level=loglevel,
                        fmt=log_format,
                        datefmt=log_datefmt,
                        isatty=True,
                        )

    # disable propagation
    log.propagate = False

    logging.info("Config:  Configuration file loading...")
    """provides facilities for managing a configuration from disk"""


def setup(filename: str) -> None:
    """
    Sets up the module by loading the specified configuration file from disk

    Args:
        filename (str): path and filename to load.
    """
    global config

    path = f"config/{filename}"
    # check if the file exists
    if os.path.exists(path):
        logging.info(f"Config:  Found a file/directory at {filename}'! attempting to load...")
        with open(path, 'r') as infile:
            config_dict = json.load(infile)
            logging.info("Config:  Successfully loaded JSON from file specified!")

        setup_logging(config_dict['logging']['log_file'])
        config = config_dict
    else:
        raise FileNotFoundError(f"Config:  unable to find {filename}")


# fetch the CLI argument
_path = cli_manager.args.config_file
# and initialize
setup(_path)
