#!/usr/bin/python3

#########################
##    SET DIRECTORY    ##
#########################

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

###################
##    IMPORTS    ##
###################

from config import APIMethod, MSSQLInfo
from classes.server import getCurrentDate
from classes.xmlParser import xmlGetDict
from classes.log import *
from db.sqlPOST import sqlTruncate
from maxoptra.authentication import createSession
from maxoptra.endpointsOrders import *
from maxoptra.endpointsObjects import *
from maxoptra.endpointsSchedules import *
from maxoptra.endpointsAutoscheduling import *
from functools import partial

################
##   GLOBAL   ##
################

# Get the session ID
sessionID = createSession()

xmlTEMPLATE = f"""<?xml version="1.0" encoding="UTF-8"?>
<apiRequest>
   <sessionID>{sessionID}</sessionID>
   <orders>"""

################
##   ORDERS   ##
################

def APIsave(xmlPOST=xmlTEMPLATE):
    if APIMethod.enableSave:
        log.info('Running Task: [Save]')
        try:
            data = sqlGET_ScheduleImport.sqlPrepare_save(MSSQLInfo.DB_APISave)
            saveXMLorder = ""
            for t_APISaveRequest in data:
                if t_APISaveRequest.bowakref != "":
                    saveXMLorder += f"""
                      <order>
                         <areaOfControl>Bowak</areaOfControl>
                         <date>{t_APISaveRequest.date}</date>
                         <client>
                            <name>{t_APISaveRequest.clientName}</name>
                            <contactPerson>{t_APISaveRequest.contactPerson}</contactPerson>
                            <contactNumber>{t_APISaveRequest.contactNumber}</contactNumber>
                            <contactEmail>{t_APISaveRequest.contactEmail}</contactEmail>
                            <enableSMSNotification>{t_APISaveRequest.enableSMSNotification}</enableSMSNotification>
                            <enableEMAILNotification>{t_APISaveRequest.enableEMAILNotification}</enableEMAILNotification>
                         </client>		 
                         <location>
                            <name>{t_APISaveRequest.customerLocationName}</name>
                            <address>{t_APISaveRequest.customerLocationAddress}</address>
                            <globalid>{t_APISaveRequest.globalid}</globalid>
                         </location>
                         <dropWindows>
                            <dropWindow>
                               <start>{t_APISaveRequest.dropWindowStart1}</start>
                               <end>{t_APISaveRequest.dropWindowEnd1}</end>
                            </dropWindow>"""
                    if t_APISaveRequest.dropWindowStart2 != "":
                        saveXMLorder += f"""<dropWindow>
                                              <start>{t_APISaveRequest.dropWindowStart2}</start>
                                              <end>{t_APISaveRequest.dropWindowEnd2}</end>
                                           </dropWindow>"""
                    if t_APISaveRequest.dropWindowStart3 != "":
                        saveXMLorder += f"""<dropWindow>
                                              <start>{t_APISaveRequest.dropWindowStart3}</start>
                                              <end>{t_APISaveRequest.dropWindowEnd3}</end>
                                           </dropWindow>"""
                    saveXMLorder += f"""</dropWindows>
                         <capacity>{t_APISaveRequest.capacity}</capacity>		 		 
                         <collection>{t_APISaveRequest.collection}</collection>		 
                         <additionalInstructions>{t_APISaveRequest.additionalInstructions}</additionalInstructions>		
                         <dynamicAttributes>
                            <attribute name="bowakref" value="{t_APISaveRequest.bowakref}" />
                         </dynamicAttributes>
                      </order>"""
            xmlPOST += saveXMLorder
            xmlPOST += """
               </orders>
            </apiRequest>"""
            if debugMode:
                log.debug(f'Using XML for [Save]:\n{xmlPOST}')
            saveOrder(xmlPOST)
            #sqlTruncate(MSSQLInfo.DB_APISave)
        except Exception as e:
            log.critical("[Save] exception: " + str(e))

def APIdelete(xmlPOST=xmlTEMPLATE):
    if APIMethod.enableDelete:
        log.info('Running Task: [Delete]')
        try:
            data = sqlGET_ScheduleImport.sqlPrepare_save(MSSQLInfo.DB_APISave)
            deleteXMLorder = ""
            for order in data:
                if order.orderReference != "":
                    deleteXMLorder += \
            f"""<order>
                    <orderReference>{order.orderReference}</orderReference>
                </order>"""
            xmlPOST += deleteXMLorder
            xmlPOST += """
               </orders>
            </apiRequest>"""
            if debugMode:
                log.debug(f'Using XML for [Save]:\n{xmlPOST}')
            deleteOrder(sessionID)
        except Exception as e:
            log.critical("[Delete] exception: " + str(e))

#################
##   OBJECTS   ##
#################

##################
##   SCHEDULE   ##
##################

def APIpostScheduleImport():
    if APIMethod.enableScheduleImport:
        log.info('Running Task: [Schedule Import]')
        try:
            postScheduleImport(sessionID)
        except Exception as e:
            log.critical("[ScheduleImport] exception: " + str(e))

##########################
##    AUTOSCHEDULING    ##
##########################

def APIstart(aocID):
    if APIMethod.enableStart:
        log.info('Running Task: [Start Request]')
        try:
            startDate = getCurrentDate()
            return startRequest(sessionID, aocID, startDate, True)
        except Exception as e:
            log.critical("[Start Request] exception: " + str(e))

########################
##    GET API DATA    ##
########################

def API_POST(argv):
    try:
        if sessionID:
            # Get the ID list of Area of Controls
            AreaOfControls = xmlGetDict(getAreaOfControls(sessionID))
            if AreaOfControls:
                AreaOfControls = AreaOfControls['apiResponse']['areaOfControlResponse']['aocs']['aoc']
                # Loop through the Area of Controls
                for aoc in AreaOfControls:
                    aocID = aoc['@id']
                    aocName = aoc['@name']
                    # Map the inputs to the function blocks
                    options = \
                        {
                            '-delete': APIdelete,
                            '-save': APIsave,
                            '-scheduleImport': APIpostScheduleImport,
                            '-start': partial(APIstart, aocID),
                        }
                    options[argv[1]]()
            else:
                log.warning('The server could not retrieve any \'AreaOfControls\'. Please review the script or API configuration.')
        else:
            log.error('The session ID could not be found or created. Please review the authentication configuration credentials.')

    except KeyError:
        log.error(f'No argument found for \'{argv[1]}\'. Please use a valid argument.')

# RUN MAIN SCRIPT
if __name__ == '__main__':
    fileName = os.path.basename(__file__)
    if len(sys.argv) < 2:
        log.warning(f"""No arguments were provided for {fileName}. Please use one the following:
            -delete
            -save            
            -scheduleImport
            -start""")
    else:
        API_POST(sys.argv)
        log.info(f'Script {fileName} successfully finished.')