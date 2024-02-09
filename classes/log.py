#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

import sys
from os import path

import logging
import traceback
import os,sys,inspect
from config import debugMode, disableSilentMode, logFileName

#######################
##    Log to file    ##
#######################

class log:
    # Get the parent directory
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    logDir = os.path.join(parent_dir,"log")
    # If log folder does not exist
    if not os.path.exists(logDir):
        os.mkdir(logDir)

    # Set the log path location
    logFileName = os.path.join(logDir,logFileName)
    logAPIFile = os.path.basename(path.abspath(sys.modules['__main__'].__file__)).replace('.py','')
    logFormat = f'%(asctime)s [{logAPIFile}] [%(levelname)s]: %(message)s'
    # For debug only
    if debugMode:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO

    # Log setup configuration
    logging.basicConfig(filename=logFileName,
                        filemode='a',
                        format=logFormat,
                        datefmt='%H:%M:%S',
                        level=logLevel)
    @staticmethod
    def critical (logMessage):
        logInfo = log.logFrame() + logMessage
        logging.critical(f"{logInfo}\n{traceback.format_exc()}")
        if disableSilentMode:
            print(f'Server: {logMessage}\n{traceback.format_exc()}')
        sys.exit(0)
    @staticmethod
    def error (logMessage):
        logInfo = log.logFrame() + logMessage
        logging.error(logInfo)
        if disableSilentMode:
            print(f'Server: {logMessage}')
    @staticmethod
    def warning(logMessage):
        logInfo = log.logFrame() + logMessage
        logging.warning(logInfo)
        if disableSilentMode:
            print(f'Server: {logMessage}')
    @staticmethod
    def info(logMessage):
        logInfo = log.logFrame() + logMessage
        logging.info(logInfo)
        if disableSilentMode:
            print(f'Server: {logMessage}')
    @staticmethod
    def debug (logMessage):
        logInfo = log.logFrame() + logMessage
        logging.debug(logInfo)
        if disableSilentMode:
            print(f'Server: {logMessage}')

    @staticmethod
    def logFrame():
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe)[2]
        fileName = calframe.filename.replace(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), '')
        return f'File: {fileName} | Function: {calframe[3]} | Message: '