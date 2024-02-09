#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

import requests
from config import APIcredentials, URL
from classes.server import URLCheck
from classes.log import log
from classes.xmlParser import xmlTree, xmlResponse

###########################
##    Get Session Key    ##
###########################

# Creates a session with the Maxoptra REST API
def createSession():
    try:
        response = requests.post(URL.createSessionURL, params=APIcredentials)
        # Check that a status code 200 is returned
        if (URLCheck(__name__, response)):
            data = xmlTree(response.text)
            # Find any error with the connection
            error = xmlResponse(data, 'errorMessage')
            if error:
                log.error("Connection Error: " + str(error))
                return
            # If no error check that response is authorised
            authResponse = xmlResponse(data, 'sessionID')
            if authResponse:
                log.info("Connection to MaxOptra successful. Using session key: " + str(authResponse))
                return authResponse
            else:
                msg = 'Server cannot determine if a session response was given.'
                log.error(msg)
                raise ValueError(msg)
        else:
            log.error("Connection Error: " + str(response.status_code))
    except Exception as e:
        log.critical("An exception occurred:" + str(e))
