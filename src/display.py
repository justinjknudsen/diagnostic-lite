#!/usr/bin/python3

import configparser
import datetime
import syslog
import sys 
import time
import Adafruit_CharLCD as LC 
import Adafruit_GPIO.MCP230xx as MCP
from diagnosticd.modules import pc_status 

#globals
CONFIG_FILE = '/usr/local/src/diagnostic-lite/conf/trex_iris_lite_template.20200305'
DIGITEMP_SENSORS = "/tmp/imager_safetyd.temperature"

LCD_RS = 0
LCD_EN = 1
LCD_D4 = 2
LCD_D5 = 3
LCD_D6 = 4
LCD_D7 = 5
LCD_RED = 6
LCD_GREEN = 7
LCD_BLUE = 8

LCD_COLUMNS = 20
LCD_ROWS = 4

GPIO = MCP.MCP23017(busnum=2)

LCD = LC.Adafruit_RGBCharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COLUMNS, LCD_ROWS, LCD_RED, LCD_GREEN, LCD_BLUE, gpio=GPIO)

def read_config(filename):
    config = None
    config = configparser.RawConfigParser()
    config.read(filename)
    return config

def main():

    #read config file
    try:
        config_file = read_config(CONFIG_FILE)
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, "Error reading config file: %s" % (str(e)))

    #iteration counter to clock first loop 
    n = [0]*5

    #main loop 
    while True:

        #current time
        current_time = datetime.datetime.now()
        seconds = current_time.second

        #network
        if config_file.get('network','run').lower() == 'true':
            cadence = config_file.getint('network','cadence')
            if (seconds%cadence) == 0 or n[0] == 0:
                network = pc_status.network()
                n[0] = 1
        else:
            network = -1
        
        #cpu_usage
        if config_file.get('cpu_usage','run').lower() == 'true':
            cadence = config_file.getint('cpu_usage','cadence')
            if (seconds%cadence) == 0 or n[1] == 0:
                time.sleep(0.1)
                cpu_usage = pc_status.cpu_usage()
                time.sleep(0.1)
                n[1] == 1
        else:
            cpu_usage = -1

        #drive_capacity
        # if config_file.get('cpu_usage','run').lower() == 'true':
        #     cadence = config_file.getint('cpu_usage','cadence')
        #     if (seconds%cadence) == 0 or n[2] == 0:
        #         drive_capactiy = pc_status.drive_capactiy()
        #         n[2] == 1
        # else:
        #     drive_capacity = -1

        #temperature
        if config_file.get('temperature','run').lower() == 'true':
            cadence = config_file.getint('temperature','cadence')
            if (seconds%cadence) == 0 or n[3] == 0:
                temperature = -1
                n[3] == 1
        else:
            temperature = -1

        #humidity
        if config_file.get('humidity','run').lower() == 'true':
            cadence = config_file.getint('humidity','cadence')
            if (seconds%cadence) == 0 or n[4] == 0:
                humidity = -1
                n[4] == 1
        else:
            humidity = -1

        #displaying info on LCD

        LCD.clear()
        LCD.message('Network: %.2fms \ncpu usage: %.2f%%' % (network,cpu_usage))
        time.sleep(10)

if __name__ == "__main__":
    syslog.openlog("diagnostic-lite")
    ret = main()
    syslog.closelog()
    sys.exit(ret)
