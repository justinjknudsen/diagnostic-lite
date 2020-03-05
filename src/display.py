#!/usr/bin/python3

import sys
import time
import Adafruit_CharLCD as LC 
import Adafruit_GPIO.MCP230xx as MCP
from diagnosticd.modules import pc_status 

#define MCP pins connected to the LCD.
LCD_RS = 0
LCD_EN = 1
LCD_D4 = 2
LCD_D5 = 3
LCD_D6 = 4
LCD_D7 = 5
LCD_RED = 6
LCD_GREEN = 7
LCD_BLUE = 8

#specifying a 20x4 LCD.
LCD_COLUMNS = 20
LCD_ROWS = 4

#Initializing the MCP device on another I2C address or bus.
GPIO = MCP.MCP23017(busnum=2)

#initialize the LCD using the pins
LCD = LC.Adafruit_RGBCharLCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COLUMNS, LCD_ROWS, LCD_RED, LCD_GREEN, LCD_BLUE, gpio=GPIO)

def main():

    while True:
        
        #calling functions
        network = pc_status.network()
        cpu_usage = pc_status.cpu_usage()
        #drive_capactiy = pc_status.drive_capactiy()

        #displaying info on LCD
        LCD.clear()
        LCD.message('network: %.2fms \ncpu usage: %s %%' % (network,cpu_usage))
        time.sleep(5)

        



if __name__ == "__main__":
    sys.exit(main())
