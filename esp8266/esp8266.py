#!/usr/bin/env python
          
import time
import serial
              
ser = serial.Serial(
      port='/dev/ttyAMA0', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)              

class esp8266(object):

    def __init__(self):
        pass

    def get_response(self):

	while 1:
        	data = ser.readline()
                print data
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
    esp.version()
    
    if args.raw != "" :
        esp.raw(cmd=args.raw)
        
    if args.scan > 0:    
	    for x in range(0, args.scan):
            	esp.scan()



