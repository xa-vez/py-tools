 #!/usr/bin/env python
          
import time
import serial
              
ser = serial.Serial(
      port='/dev/ttyAMA0', baudrate = 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)              


class esp8266(object):
    def __init__(self):
        pass

    def version(self):
            ser.write('AT+GMR\r\n')
            time.sleep(1)
            x=ser.readall()
            print x
                
    def scan(self, qty):
    
        while qty > 0 :
            ser.write('AT+CWLAP\r\n')
            time.sleep(5)
            x=ser.readall()
            print x
            qty -= 1
            

        
if __name__== "__main__":
    import argparse

    options = argparse.ArgumentParser()
    #options.add_argument('-p', "--pdn", type=int, choices=[1,2,3], default=1, help="The PDN number")
    #options.add_argument('-l', "--lpm", type=int, choices=[1,2,3], default=1, help="The low power mode")
    #options.add_argument('-s', "--scan", type=str, default="", help="scan networks")
    options.add_argument('-s', "--scan", type=int, default=1, help="scan networks -n times")
    options.add_argument('-v', "--verbose", action="store_true", help="verbose mode")

    args = options.parse_args()
        
    if args.verbose :
        #print( 'verbose mode is runnig ' + args.domain + ' at PDN ' + str(args.pdn))
        print('verbose mode')

    esp = esp8266()
    esp.version()
        
    if args.scan :    
        esp.scan(2)

