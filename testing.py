#! /usr/bin/env python

# using this and not changing structure so that lcd can be cloned 
# may want to do something else at some point
#import sys
#sys.path.append('/home/pi/rasberrypi_for_spinmaster/spinmaster_lcd/lcd/')

import drivers
from time import sleep
#from datetime import datetime
from subprocess import check_output
import os

display = drivers.Lcd()
first_run = False

'''
def long_string(display, text='', num_line=1, num_cols=16):
    """
    Parameters: (driver, string to print, number of line to print, number of columns of your display)
    Return: This function send to display your scrolling string.
    """
    if len(text) > num_cols:
        display.lcd_display_string(text[:num_cols], num_line)
        sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i + num_cols]
            display.lcd_display_string(text_to_print, num_line)
            if not i % 16:
                sleep(2)
        sleep(2)
    else:
        display.lcd_display_string(text, num_line)
'''

try:
    '''
    if "SPINMASTER_LCD_FIRST_RUN" not in os.environ: #TDO make this not happen every time
        display.lcd_display_string("   SpinMaster  ", 1)
        os.putenv("SPINMASTER_LCD_FIRST_RUN", "1")
    display.lcd_display_extended_string(str(datetime.now()), 2)
    sleep(5)
    '''
    
    if len(check_output(["hostname", "-I"]).split()):
            print("Got IP")
            IP = check_output(["hostname", "-I"]).split()[0].decode('UTF-8')
            display.lcd_display_string("                ", 2)
            display.lcd_display_string(str(IP), 2)
    else:
            print("No IP")
            display.lcd_display_string("  Offline  ", 2)

    sleep(10)
    display.lcd_clear()
    
    #change with: echo SPINMASTER_RUNNING=1 > ./spinmaster_lcd/enviroment_variables_for_lcd_service
    #TO: don't overwrite entire file just edit line
    '''
    if "SPINMASTER_RUNNING" in os.environ and int(os.environ.get("SPINMASTER_RUNNING")) != 0:
        display.lcd_display_string("    Running    ", 2)
    else:
        display.lcd_display_string("    Standby    ", 2)
        sleep(2)
        long_string(display, "Please see web based control panel at displayed IP", 2)

    sleep(2)
'''

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
#    print("Cleaning up!")
    display.lcd_clear()