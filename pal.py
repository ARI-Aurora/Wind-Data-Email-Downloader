import logging
import sys

def setupLogging(name: str) -> logging.Logger:
    pal = logging.getLogger(name)
    pal.setLevel(logging.DEBUG)
    logFile = logging.FileHandler('/root/wded.log')
    logFile.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s'))
    consoleLog = logging.StreamHandler(sys.stdout)
    consoleLog.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(name)s: %(message)s'))
    pal.addHandler(logFile)
    pal.addHandler(consoleLog)
    pal.debug(name + " Initialized")
    return pal
