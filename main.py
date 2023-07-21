#!/usr/bin/python3
import pyodbc
import wiringpi as GPIO
from time import sleep

"""
SERVER SETUP
"""
dsn = 'myserverdatasource'
user = 'iot-device'
password = '123456789'
database = 'dserp200'

con_string = 'DSN=%s;UID=%s;PWD=%s;DATABASE=%s;'%(dsn,user,password,database)

sleep(5)        #important for startup routine to wait for ODBC service to start first
cnxn = pyodbc.connect(con_string)

global cursor
cursor = cnxn.cursor()
print('Server connected')

"""
GPIO SETUP
"""
AC_pin=4                    #AC power fault detection pin at 
DC_pin=2                    #Alarm fault detection pin at 
pAC_state = 0               #previous AC state
pDC_state = 0               #previous DC state
GPIO.wiringPiSetup()
GPIO.pinMode(AC_pin,0)
GPIO.pinMode(DC_pin,0)
print('GPIO setup complete')

"""
Initilize the value at database
"""
AC_state = 0
DC_state = 0
cursor.execute("UPDATE sysdiagrams SET principal_id ="+str(AC_state) +"where name = 'MCAS1'")
cnxn.commit()
cursor.execute("UPDATE sysdiagrams SET diagram_id ="+str(DC_state) +"where name = 'MCAS1'")
cnxn.commit()



while True:
    AC_state = GPIO.digitalRead(AC_pin)
    DC_state = GPIO.digitalRead(DC_pin)
    if not AC_state == pAC_state:
        print(f'AC_state {AC_state}')
        cursor.execute('UPDATE sysdiagrams SET principal_id ='+str(AC_state)+'where name =\'MCAS1\'')
        cnxn.commit()
        pAC_state = AC_state
    if not DC_state == pDC_state:
        print(f'                                    DC_state {DC_state}')
        cursor.execute('UPDATE sysdiagrams SET diagram_id ='+str(DC_state)+'where name =\'MCAS1\'')
        cnxn.commit()
        pDC_state = DC_state
    sleep(0.5)
        
