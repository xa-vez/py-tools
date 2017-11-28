#!/usr/bin/python3
# $sudo apt-get install python3-serial
# $sudo chmod 666 /dev/ttyUSB0
import serial
import time

class Modem(object):

    def __init__(self):
        pass
    
    def Flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        
    def Open(self):
        
        #self.ser = serial.Serial('/dev/ttyUSB0', baudrate=921600, timeout=1 )
        
        #self.ser = serial.Serial('/dev/ttyUSB0', baudrate=921600,
        #                          bytesize=8, parity='N', stopbits=1, 
        #                          timeout=1, rtscts=False )
                
        #self.ser = serial.Serial('/dev/ttyUSB0', baudrate=921600,timeout=1,
        #                          parity=serial.PARITY_NONE, rtscts=1 )
        self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200,timeout=1 )        
        #self.Flush()
        self.ser.setRTS(False)
    
    def Close(self):

        self.ser.setRTS(True)
        self.ser.close()
        
    def InitModem(self):
        
        while( True ) :
        
            if (self.SendCommand('AT\r\n' ) == False ): break
            if (self.SendCommand('at!="showver"\r\n' ) == False): break  #show version
            #if (self.SendCommand('ATE0\r')  # disable verbose mode
            if (self.SendCommand('AT+CMEE=2\r\n' ) == False ): break # enable verbose mode
            if (self.SendCommand('AT+CFUN=1\r\n') == False ): break  # configure the full functionality level
            
            return True

        return False
    
    def ConfigurLowPowerMode(self, lpm=1):
        
        while(True):
            
            if ( lpm == 1 or lpm == 2):
                if (self.SendCommand('AT+CPSMS=0\r\n' ) == False ): break
            if ( lpm == 3 ):
                if (self.SendCommand('AT+CPSMS=1,,,\"00000001\",\"00000010\"\r\n' ) == False ): break
            
            if (self.SendCommand('AT!="setlpm airplane=1 enable=1"\r\n') == False ): break   
            
            return True
        
        return False  
    
    def ConfigureSocket(self, pdn=1, lpm=1):
            
        while(True):
            if (self.SendCommand('AT+CGACT=1,' + pdn + '\r\n') == False ): break
            if (self.SendCommand('AT+SQNSCFG=1,'+ pdn + ',0,0,600,50\r\n', wait=True) == False ): break
            if (self.SendCommand('AT+SQNSCFGEXT=1,1,0,0,0,0\r\n', wait=True) == False): break
            
            if ( lpm == 2):
            #if (self.SendCommand('AT+CEDRXS=2,4,\"0010\"\r\n', wait=True, response='+CEDRXP') == -1 ): break 
                if (self.SendCommand('AT+CEDRXS=2,4,\"0010\"\r\n', wait=True) == False ): break
            if ( lpm == 3 ):
                if (self.SendCommand('AT+CPSMS=?\r\n' ) == False ): break
            
            return True
        
        return False
        
    
        
    def SendCommand(self, command, wait=False, getline=False, response='OK' ):
        print(command)
        self.ser.write(command.encode())
        data = ''
        result = False
        
        if ( wait == True ):
            time.sleep(2)   
            
        if ( getline == True ): 
            data = self.ReadLine()
        else :
            data = self.ReadAll()
                        
        if ( len(response) > 0 ):
            if (data.find(response.encode()) > 0 ):
                result = True
            
        return result

    def ReadLine(self):
        data = self.ser.readline()  
        print (data)
        return data 

    def ReadAll(self):
        data = self.ser.readall()  
        print (data)
        return data 

    def ResetModem(self) :
        self.SendCommand('AT^RESET\r\n')
        
     
    def Test(self, pdn, domain, lpm):
            
        print( time.asctime() + ' [ Test running... ] ' + 'LMP: ' + str(lpm) )
        
        self.Open()
        self.InitModem()
        self.ConfigurLowPowerMode(lpm)
        self.ConfigureSocket(pdn, lpm)
        self.Close()
            
        while( True ):
            
            self.Open()
         
            ######################
            if (self.SendCommand('AT+CEREG?\r\n', response='+CEREG') == False ): break #Network Registration status
            if (self.SendCommand('AT+CGACT?\r\n') == False): break  # PDP Context activate ? 
            if (self.SendCommand('AT+SQNSS\r\n') == False ): break  # Socket status
            ######################
             
            self.SendCommand('at+sqnsd=1,0,80,"'+domain+'",0,0,1\r\n', wait=True) # can also be 172.217.1.238" 
            self.SendCommand('at+sqnssend=1\r\n', wait=True, response='>') 
            self.SendCommand('GET / HTTP/1.1\r\nHost:'+domain+'\r\n\r\n\032', wait=True, response='+SQNSRING') # this might take time
            self.SendCommand('at+sqnsrecv=1,1500\r\n') # receive from socket
             
            if ( lpm == 3 ):
                if (self.SendCommand('at+sqnsh=1\r\n') == False ): break # shutdown the socket
        
            wnc.Close()
            
            print( time.asctime() + ' [ Test passed ]')
            #return
            time.sleep(60)
            
        #wnc.ResetModem()
        wnc.Close()
        print(time.asctime() + ' [ Test Failed ]')
    
if __name__ == "__main__":
    import argparse

    options = argparse.ArgumentParser()
    options.add_argument('-p', "--pdn", type=int, choices=[1,2,3], default=1, help="The PDN number")
    options.add_argument('-d', "--domain", type=str, default="google.com", help="The domain ex: google.com")
    options.add_argument('-l', "--lpm", type=int, choices=[1,2,3], default=1, help="The low power mode")
    options.add_argument('-v', "--verbose", action="store_true", help="verbose mode")
    
    args = options.parse_args()
 
    if args.verbose :
        print( 'trying to connect to ' + args.domain + ' at PDN ' + str(args.pdn))
    
    wnc = Modem()
    wnc.Test(pdn=str(args.pdn), domain=args.domain, lpm=args.lpm)
