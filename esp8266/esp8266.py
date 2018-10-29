#!/usr/bin/env python
          
import serial
import time
import datetime

CRED = '\033[91m'
CGREEN = '\033[92m'
CBLUE = '\033[94m'
CCYAN = '\033[96m'
CWHITE = '\033[97m'
CYELLOW = '\033[93m'
CMAGENTA = '\033[95m'
CGREY = '\033[90m'
CBLACK = '\033[90m'
CDEFAULT = '\033[99m'
CEND = '\033[0m'
              
ser = serial.Serial(
    port='/dev/ttyAMA0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)              

class esp8266(object):

    def __init__(self):
        pass

    def get_response(self):
        while 1: 
           data = ser.readline()
           print(data.replace("\r\n", ''))
           if (data == "ERROR\r\n") : break
           if (data == "OK\r\n") : break

    def version(self):
        ser.write('AT+GMR\r\n')
        self.get_response()

    def scan(self):
        ser.write('AT+CWLAP\r\n')
        self.get_response()

    def raw(self, cmd):
        ser.write(cmd + '\r\n')
        self.get_response()

if __name__ == "__main__":
    import argparse

    options = argparse.ArgumentParser()
    options.add_argument('-r', "--raw", type=str, default="", help="raw command")
    options.add_argument('-s', "--scan", type=int, default=0, help="scan networks -n times")
    options.add_argument('-v', "--verbose", action="store_true", help="verbose mode")
    args = options.parse_args()

    esp = esp8266() 
    print CCYAN + '['+ str(datetime.datetime.now()) + ']' + ' [ESP8266] Executing Version' + CEND + '\r\n'
    esp.version()
    print CCYAN +'['+ str(datetime.datetime.now()) + ']' + ' [ESP8266] End Version' + CEND + '\r\n'

    if args.raw != "" :
        print CCYAN + '['+ str(datetime.datetime.now()) + ']' + ' [ESP8266] Executing Raw Command' + CEND + '\r\n'
        esp.raw(cmd=args.raw)
        print CCYAN + '['+ str(datetime.datetime.now()) + ']' + ' [ESP8266] End command' + CEND + '\r\n'

    if args.scan > 0:    
        for x in range(0, args.scan):
            print CCYAN + '['+ str(datetime.datetime.now()) + ']' + ' [ESP8266] Round: ' + str(x+1) + CEND +'\r\n' 
            esp.scan()
            print CCYAN + '['+ str(datetime.datetime.now()) + ']' + ' [ESP8266] End round' + CEND + '\r\n'

