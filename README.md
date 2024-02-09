# Maxoptra API

Python script to collect data and schedule deliveries & collections with Maxoptra via their REST API Version 2.
API Documentation: https://doc.maxoptra.com/docs/display/MX/REST+API

## Installation

To install this script simply deploy the full contents to any directory on a server. The server will need either a SQL server, or connectivity to a SQL server.
The server must be a Microsoft SQL server. This script is not compatable with MySQL.

## Requirement Moduals

The following moduals will need to be installed, which are not standard with Python:

- pyodbc
- requests
- schedule
- xmltodict
- dict2xml

Use: `pip install module_name` in command prompt to install any missing modules.

## Usage :computer:

The API script has two main components located both in the `API` folder. The two components are:

- API_GET.py
- API_POST.py

`API_GET.py` is only used to collect data from the MaxOptra. This receives the XML response from the API and inserts the data to a MSSQL server. Two arguments can be given, depending on what you wish to do:

- -runDaily
- -runOnDemand

`-runDaily` requests data from the API from a greater length of time, and is used for daily update, rather than on demand updates. The length of time the system looks back from the current date is specified in the `config.py` file named `dailyScheduleHistoryDays`.

`-runOnDemand` disables the scripts own internal method of running every minuet to collect data.

If no arguments are passed, the script will default to updating the SQL server every minute until cancelled.

`API_POST.py` Is used to preform API related commands and uploading of data to MaxOptra. This can either POST and XML save request or send a command to MaxOptra to start or stop events. The following arguments can be given the script:

- -delete
- -save
- -scheduleImport
- -start

`-delete` requests to delete an order in Maxoptra.

`-save` creates and updates orders in Maxoptra, API uses application/xml as its acceptable request representation, and the standard HTTP-method POST

`-scheduleImport` this request is used to import schedules to the system. To import schedules to Maxoptra, API uses application/xml as its acceptable request representation, and the standard HTTP-method POST.

`-start` the API uses start method to start autoscheduling for a specific distribution centre (or several DCs).

The script requires only one argument. No more than one can be provided, if none are provided the script will terminate.

## Confiuration :wrench:

All configuration changes are made in the `config.py` file.

```python
APIcredentials = {
    'accountID' : 'YOUR_ACCOUNT_ID',       # Maxoptra Account Id
    'user' : 'YOUR_USERS_EMAIL_ADDRESS',   # Maxoptra Username
    'password' : 'YOUR_USERS_PASSWORD'     # Maxoptra Password
}


class MSSQLInfo:
    DB_Driver =             'ODBC Driver 17 for SQL Server'
    DB_Server =             'Localhost'
    DB_Name =               'DB_NAME'
    DB_UserName =           'DB_USERNAME'
    DB_Password =           'DB_PASSWORD'
    DB_Trusted_Connection = 'yes'

    # Name of API table for 'Request Daily'
    DB_APIDaily = ''
    # Name of API table for 'Request Current'
    DB_APICurrent = ''
    # Name of API table for 'Saved data to upload'
    DB_APISave = ''
```
