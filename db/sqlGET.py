#!/usr/bin/python3

###################
##    IMPORTS    ##
###################

from config import debugMode, MSSQLInfo
from classes.log import log
from db.connector import MSSQL

class sqlGET_ScheduleImport:
    ###################
    ##    GLOBALS    ##
    ###################
    @staticmethod
    def sqlPrepare_save(table):
        sqlQuery = f"""
        SELECT
           REPLACE(ISNULL([bowakref],''),CHAR(13)+CHAR(10),'') AS [bowakref]
          ,REPLACE(FORMAT(ISNULL([date],''),'dd/MM/yyyy'),CHAR(13)+CHAR(10),'') AS [date]
          ,REPLACE(ISNULL([customerLocationName],''),CHAR(13)+CHAR(10),'') AS [customerLocationName]
          ,REPLACE(ISNULL([customerLocationAddress],''),CHAR(13)+CHAR(10),'') AS [customerLocationAddress]
          ,REPLACE(ISNULL([capacity],''),CHAR(13)+CHAR(10),'') AS [capacity]
          ,REPLACE(ISNULL([distributionCentreName],''),CHAR(13)+CHAR(10),'') AS [distributionCentreName]
          ,REPLACE(ISNULL(FORMAT([dropWindowStart1],'dd/MM/yyyy HH:mm'),''),CHAR(13)+CHAR(10),'') AS [dropWindowStart1]
          ,REPLACE(ISNULL(FORMAT([dropWindowEnd1],'dd/MM/yyyy HH:mm'),''),CHAR(13)+CHAR(10),'') AS [dropWindowEnd1]
          ,REPLACE(ISNULL(FORMAT([dropWindowStart2],'dd/MM/yyyy HH:mm'),''),CHAR(13)+CHAR(10),'') AS [dropWindowStart2]
          ,REPLACE(ISNULL(FORMAT([dropWindowEnd2],'dd/MM/yyyy HH:mm'),''),CHAR(13)+CHAR(10),'') AS [dropWindowEnd2]
          ,REPLACE(ISNULL(FORMAT([dropWindowStart3],'dd/MM/yyyy HH:mm'),''),CHAR(13)+CHAR(10),'') AS [dropWindowStart3]
          ,REPLACE(ISNULL(FORMAT([dropWindowEnd3],'dd/MM/yyyy HH:mm'),''),CHAR(13)+CHAR(10),'') AS [dropWindowEnd3]
          ,REPLACE(ISNULL([clientName],''),CHAR(13)+CHAR(10),'') AS [clientName]
          ,REPLACE(ISNULL([contactPerson],''),CHAR(13)+CHAR(10),'') AS [contactPerson]
          ,REPLACE(ISNULL([contactNumber],''),CHAR(13)+CHAR(10),'') AS [contactNumber]
          ,REPLACE(ISNULL([contactEmail],''),CHAR(13)+CHAR(10),'') AS [contactEmail]
		  ,CASE
			WHEN [enableSMSNotification] > 1 THEN 'true'
			WHEN [enableSMSNotification] > 0 THEN 'false'
			ELSE 'false'
		   END AS [enableSMSNotification]
		  ,CASE
			WHEN [enableEMAILNotification] > 1 THEN 'true'
			WHEN [enableEMAILNotification] > 0 THEN 'false'
			ELSE 'false'
		   END AS [enableEMAILNotification]
		  ,CASE
			WHEN [collection] > 1 THEN 'true'
			WHEN [collection] > 0 THEN 'false'
			ELSE 'false'
		   END AS [collection]
          ,REPLACE(ISNULL([additionalInstructions],''),CHAR(13)+CHAR(10),'') AS [additionalInstructions]
          ,REPLACE(ISNULL([globalid],''),CHAR(13)+CHAR(10),'') AS [globalid]
        FROM 
            [{MSSQLInfo.DB_Name}].[dbo].[{table}]"""

        if debugMode:
            log.debug(f'Server executed SQL query: {sqlQuery}')
        MSSQL.execute(sqlQuery)
        return MSSQL.fetchall()

    @staticmethod
    def sqlGetDateRange(table):
        sqlQuery = f"""
        SELECT
            REPLACE(ISNULL(FORMAT([{MSSQLInfo.DB_APIDateRange_ColumnStartDateName}],'dd/MM/yyyy'),''),CHAR(13)+CHAR(10),'') AS [{MSSQLInfo.DB_APIDateRange_ColumnStartDateName}],
            REPLACE(ISNULL(FORMAT([{MSSQLInfo.DB_APIDateRange_ColumnEndDateName}],'dd/MM/yyyy'),''),CHAR(13)+CHAR(10),'') AS [{MSSQLInfo.DB_APIDateRange_ColumnEndDateName}]
        FROM 
            [{MSSQLInfo.DB_Name}].[dbo].[{table}]"""

        if debugMode:
            log.debug(f'Server executed SQL query: {sqlQuery}')
        MSSQL.execute(sqlQuery)
        return MSSQL.fetchall()