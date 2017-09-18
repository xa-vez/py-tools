#!/usr/bin/python3
import serial
import time

class Modem(object):

    def __init__(self):
        pass
    
    def Flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        
    def Open(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.Flush()

    def Close(self):
        self.ser.close()
        
    def SendCommand(self, command, wait=False, getline=False, response='' ):
        self.ser.write(command.encode())
        data = ''
  
        if ( wait == True ):
            time.sleep(1)   
            
        if ( getline == True ): 
            data = self.ReadLine()
        else :
            data = self.ReadAll()
                        
        if ( len(response) > 0 ):
            if (data.find(response.encode()) == -1 ):
                data = -1
            
        return data 

    def ReadLine(self):
        data = self.ser.readline()  
        print (data)
        return data 

    def ReadAll(self):
        data = self.ser.readall()  
        print (data)
        return data 

    def Test(self, pdn, domain):
        
        while(True):
            if (self.SendCommand('AT\r\n' ) == -1 ): break
            if (self.SendCommand('at!="showver"\r\n' ) == -1 ): break  #show version
            #if (self.SendCommand('ATE0\r')  # disable verbose mode
            if (self.SendCommand('AT+CMEE=2\r\n' ) == -1 ): break # enable verbose mode
            if (self.SendCommand('AT+CPSMS=0\r\n' ) == -1 ): break
            if (self.SendCommand('AT+CFUN=1\r\n') == -1 ): break  # configure the full functionality level
            if (self.SendCommand('AT!="setlpm airplane=1 enable=1"\r\n') == -1 ): break
            if (self.SendCommand('AT+CGACT=1,' + pdn + '\r\n') == '' ): break
            if (self.SendCommand('AT+SQNSCFG=1,'+ pdn + ',0,0,600,50\r\n') == -1 ): break
            if (self.SendCommand('AT+SQNSCFGEXT=1,1,0,0,0,0\r\n') == '' ): break
            if (self.SendCommand('AT+CEREG?\r\n') == -1 ): break
            if (self.SendCommand('AT+CGACT?\r\n') == -1 ): break
            if (self.SendCommand('AT+SQNSS\r\n') == -1 ): break
            
            if (self.SendCommand('at+sqnsd=1,0,80,"'+domain+'",0,0,1\r\n') == -1 ): break # can also be 172.217.1.238" 
            if (self.SendCommand('at+sqnssend=1\r\n', wait=True, response='>') == -1 ): break
            if (self.SendCommand('GET / HTTP/1.1\r\nHost:'+domain+'\r\n\r\n') == -1 ): break # this might take time
            if (self.SendCommand('\032', wait=True, response='+SQNSRING') == -1 ): break
            if (self.SendCommand('at+sqnsrecv=1,1500\r\n') == '' ): break# receive from socket
            if (self.SendCommand('at+sqnsh=1\r\n') == -1 ): break # shutdown the socket
    
            print( time.asctime() + ' [ Test passed ]')
            return
    
        print(time.asctime() + ' [ Test Failed ]')
    
if __name__ == "__main__":
    import argparse

    options = argparse.ArgumentParser()
    options.add_argument('-p', "--pdn", type=int, choices=[1,2,3], default=3, help="The PDN number")
    options.add_argument('-d', "--domain", type=str, default="google.com", help="The domain ex: google.com")
    options.add_argument('-v', "--verbose", action="store_true", help="verbose mode")
    
    args = options.parse_args()
 
    if args.verbose :
        print( 'trying to connect to ' + args.domain + ' at PDN ' + str(args.pdn))
    
    wnc = Modem()
    wnc.Open()  
    wnc.Test(pdn=str(args.pdn), domain=args.domain)
    wnc.Close()

      
