#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from classes.server import getAPIData
from config import URL

####################################
##    Connection API Endpoints    ##
####################################

def getAreaOfControls(sessionID):
    return getAPIData(URL.getAreaOfControlsURL, {'sessionID' : sessionID })

def getVehicles(sessionID, date):
    return getAPIData(URL.getVehiclesURL, {'sessionID' : sessionID, 'date' : date})

def getVehiclesByAoc (sessionID, date, aocID):
    return

def getPerformers(sessionID, date, aocID):
    return getAPIData(URL.getPerformersURL, {'sessionID' : sessionID, 'date' : date, 'aocID' : aocID})

def exportPerformers(sessionID):
    return getAPIData(URL.exportPerformersURL, {'sessionID' : sessionID})

def exportVehicles(sessionID):
    return getAPIData(URL.exportVehiclesURL, {'sessionID' : sessionID})