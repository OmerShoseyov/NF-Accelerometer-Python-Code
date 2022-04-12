#!/usr/bin/env python3
import drivers
from time import sleep
from subprocess import check_output
import os

display = drivers.Lcd()
first_run = False


try:
    if len(check_output(["hostname", "-I"]).split()):
            #print("Got IP")
            IP = check_output(["hostname", "-I"]).split()[0].decode('UTF-8')
            display.lcd_display_string("         ", 2)
            display.lcd_display_string("IP:" + str(IP), 2)
    else:
            #print("No IP")
            display.lcd_display_string("  Offline  ", 2)

    sleep(10)
    display.lcd_clear()

except KeyboardInterrupt:
    display.lcd_clear()