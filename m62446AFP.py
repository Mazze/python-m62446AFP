#! /bin/python3

import gpiozero
import time
import math


class m62446AFP:
    _volumeLCh=0
    _volumeRCh=0
    _volumeCCh=0
    _volumeSwCh=0
    _volumeSlCh=0
    _volumeSrCh=0
    _tleble=0
    _bass=0
    _toneByPass=0
    _output1=0
    _output2=0
    _output3=0
    _output4=0
    #Not controled by absolute values, but relative
    _masterVolume=0
    _balanceFront=0
    _balanceBack=0
    _balanceCenter=1
    _balanceSubwoofer=1
    _balanceFrontToBack=0
    _devName="M62446AFP"
    _logLevel=2

    def log(self, level, message):
        """Logs events
        Parameters 
        ----------
        level: 0=error, 1=warning, 2=info
        """
        if level==0:
            #Error
            raise Exception("from {} : {}".format(self._devName,message) ) 
        elif level==1 & self._logLevel>=1:
            #Error
            raise Warning("from {} : {}".format(self._devName,message) )
        elif  self._logLevel>=2 : 
            print("Information from {} : {}".format(self._devName,message))

    def __init__(self,latchPin=17,clockPin=27,dataPin=22):
        self.gpioLatch = gpiozero.OutputDevice(17)
        self.gpioClock = gpiozero.OutputDevice(27)
        self.gpioData  = gpiozero.OutputDevice(22)
        self.gpioamp   = gpiozero.OutputDevice(24)
        self.gpioamp.on()
        
    def __sendWord(self,word):
        self.log(2,"Send to device ")
        self.gpioLatch.on()
        usleep = lambda x: time.sleep(x/1000000.0)
        usleep(50)
        self.gpioLatch.off()
        usleep(50)
        for i in range(0,16):
            if(word&int('0b1000000000000000',2)>>i):
                print("1",end='')
                self.gpioData.on()
                usleep(50)
                self.gpioClock.on()
                usleep(50)
                self.gpioClock.off()
                usleep(50)
                self.gpioData.off()
            else:
                print("0",end='')
                self.gpioData.off()
                usleep(50)
                self.gpioClock.on()
                usleep(50)
                self.gpioClock.off()
                usleep(50)
                self.gpioData.off()
        self.gpioLatch.on()
        usleep(50)
        self.gpioLatch.off()
        self.log(2,"send done")
    
    def setVolumeLeft(self,left):
        self._volumeLCh=left
        
    def setVolumeRight(self,right):
        self._volumeRCh=right
                
    def setVolume(self,left,right):
        self._volumeLCh=left
        self._volumeRCh=right

    def setSurroundVolume(self,left,right):
        self._volumeSlCh=left
        self._volumeSrCh=right

    def setCenterVolume(self,center):
        self._volumeCCh=center
        
    def setSubwooferVolume(self,sub):
        self._volumeSwCh=sub
    
    def setOutput(self,id, state ):
        if(id==1):
            self._output1=state
        elif(id==2):
            self._output2=state
        elif(id==3):
            self._output3=state
        elif(id==4):
            self._output4=state
        else :
            self.log(0,"Unkown output {}".format(id))

    def setTleble (self, db ):
        self._tleble=db
    
    def setBase (self, db ):
        self._bass=db


    def _convertToVol(self,vol):
        # -79 Linear
        if (vol<=0) &(vol>=-79):
            value = int(-vol)
        elif (vol<=-80) &(vol>=-95):
            value = int(-(vol +80) )| int('0b1100000',2)
            #8 0 + 11000000 =>95
        else :
            #  else (-inf) 1010000
            value=int('0b1010000',2)
        return value

    def setSlot2(self):
        self.log(2,"Left: {}, right: {}".format(self._volumeLCh,self._volumeRCh))
        v1=int(self._convertToVol(self._volumeLCh))
        v2=int(self._convertToVol(self._volumeRCh))
        v3=int('0b0000000000000001',2) | v1<<9 | v2<<2
        self.__sendWord(v3)

    def setSlot3(self):
        self.log(2,"Center: {}, Sw: {}".format(self._volumeCCh,self._volumeSwCh))
        v1=int(self._convertToVol(self._volumeCCh))
        v2=int(self._convertToVol(self._volumeSwCh))
        v3=int('0b0000000000000010',2) | v1<<9 | v2<<2
        self.__sendWord(v3)

    def setSlot4(self):
        self.log(2,"Surround Left: {}, right: {}".format(self._volumeSlCh,self._volumeSrCh))
        v1=int(self._convertToVol(self._volumeSlCh))
        v2=int(self._convertToVol(self._volumeSrCh))
        v3=int('0b0000000000000011',2) | v1<<9 | v2<<2
        self.__sendWord(v3)

    def setSlot1(self):
        value=0
        # done as if because it's not logic at the end
        if self._tleble==-14:
            value = int('0b1111000000000000',2)
        elif self._tleble==-12:
            value = int('0b1101000000000000',2)
        elif self._tleble==-10:
            value = int('0b1110000000000000',2)
        elif self._tleble==-8:
            value = int('0b1100000000000000',2)
        elif self._tleble==-6:
            value = int('0b1011000000000000',2)
        elif self._tleble==-4:
            value = int('0b1010000000000000',2)
        elif self._tleble==-2:
            value = int('0b1001000000000000',2)
        elif self._tleble==0:
            value = int('0b0000000000000000',2)
        elif self._tleble==2:
            value = int('0b0001000000000000',2)
        elif self._tleble==4:
            value = int('0b0010000000000000',2)
        elif self._tleble==6:
            value = int('0b0011000000000000',2)
        elif self._tleble==8:
            value = int('0b0100000000000000',2)
        elif self._tleble==10:
            value = int('0b0110000000000000',2)
        elif self._tleble==12:
            value = int('0b0101000000000000',2)
        elif self._tleble==14:
            value = int('0b0111000000000000',2)
        else :
            print("Trible out of range")
            value = int('0b0000000000000000',2)

        v=value

        if self._bass==-14:
            value = int('0b0000000011110000',2)
        elif self._bass==-12:
            value = int('0b0000000011010000',2)
        elif self._bass==-10:
            value = int('0b0000000011100000',2)
        elif self._bass==-8:
            value = int('0b0000000011000000',2)
        elif self._bass==-6:
            value = int('0b0000000010110000',2)
        elif self._bass==-4:
            value = int('0b0000000010100000',2)
        elif self._bass==-2:
            value = int('0b0000000010010000',2)
        elif self._bass==0:
            value = int('0b0000000000000000',2)
        elif self._bass==2:
            value = int('0b0000000001000000',2)
        elif self._bass==4:
            value = int('0b0000000001000000',2)
        elif self._bass==6:
            value = int('0b0000000001100000',2)
        elif self._bass==8:
            value = int('0b0000000001000000',2)
        elif self._bass==10:
            value = int('0b0000000001100000',2)
        elif self._bass==12:
            value = int('0b0000000001010000',2)
        elif self._bass==14:
            value = int('0b0000000001110000',2)
        else :
            print("Trible out of range")
            value = int('0b0000000000000000',2)
        
        v=v|value
        if self._output1:
            v=v|int('0b0000100000000000',2)
        if self._output2:
            v=v|int('0b0000010000000000',2)
        if self._output3:
            v=v|int('0b0000001000000000',2)
        if self._output4:
            v=v|int('0b0000000100000000',2)

        if self._toneByPass:
            v=v|int('0b0000000000000100',2)
        self.__sendWord(v)

    
    def updateDevice(self):    
        self.setSlot1()
        self.setSlot2()
        self.setSlot3()
        self.setSlot4()

    
    def setBalanceFront(self, balance):
        """Set the balance between left and right in front
        
        Parameters 
        ----------
        balance: 0 is centered, -1 is full left and 1 is full right
        """
        if(balance>=-1.0)&(balance<=1.0):
            self._balanceFront=balance
        else:
            self.log(1,"Front balance  out of range -1 to 1, value given {}".format(vol) )   


    def setBalanceBack(self, balance):
        """Set the balance between left and right in back
        
        Parameters 
        ----------
        balance: 0 is centered, -1 is full left and 1 is full right
        """
        if(balance>=-1.0)&(balance<=1.0):
            self._balanceBack=balance
        else:
            self.log(1,"Back balance  out of range -1 to 1, value given {}".format(vol) )    


    def setBalanceFrontToBack(self, balance):
        """Set the balance between the front and back channels 
        
        Parameters 
        ----------
        balance: 0 is centered, -1 is full back and 1 is full front
        """
        if(balance>=-1.0)&(balance<=1.0):
            self._balanceFrontToBack=balance
        else:
            self.log(1,"Front to back volume out of range -1 to 1, value given {}".format(vol) )        
        
    
    def setBalanceCenter(self, balance):
        """Set the balance of center with respect to master
        
        Parameters 
        ----------
        balance: Multiple of master (0=off,1=as master)
        """
        if(balance>=0.0)&(balance<=1.0):
            self._balanceCenter=balance
        else:
            self.log(1,"Center volume out of range 0 - 1, value given {}".format(vol) )
        

    def setBalanceSubwoofer(self, balance):
        """Set the balance of subwoofer with respect to master
        
        Parameters 
        ----------
        balance: Multiple of master (0=off,1=as master)
        """
        if(balance>=0.0)&(balance<=1.0):
            self._balanceSubwoofer=balance
        else:
            self.log(1,"Subwoofer volume out of range 0 - 1, value given {}".format(vol) )

         

    def setMasterVolume(self, vol):
        """Set the master volume in percent
        
        Parameters 
        ----------
        balance: 0 of, 1 full
        """
        if(vol>=0.0)&(vol<=1.0):
            self._masterVolume=vol
        else:
            self.log(1,"Master volume out of range 0 - 1, value given {}".format(vol) )

    def updateRelativeVolume(self):
        """Updates all absolute Volume values based on the relative.
            Call to submit new balance settings.
        """ 
        _volumeLCh=self._masterVolume* min([(1.0-self._balanceFront),1])*min([(1.0+self._balanceFrontToBack),1])
        _volumeRCh=self._masterVolume* min([(1.0+self._balanceFront),1])*min([(1.0+self._balanceFrontToBack),1])
    
        _volumeSlCh=self._masterVolume* min([(1.0-self._balanceBack),1])*min([(1.0-self._balanceFrontToBack),1])
        _volumeSrCh=self._masterVolume* min([(1.0+self._balanceBack),1])*min([(1.0-self._balanceFrontToBack),1])

        _volumeCCh=self._masterVolume* self._balanceCenter
        _volumeSwCh=self._masterVolume* self._balanceSubwoofer
        # convert to interge
        self._volumeLCh= math.floor(-96+ 96*_volumeLCh)
        self._volumeRCh= math.floor(-96+ 96*_volumeRCh)
        self._volumeSlCh= math.floor(-96+ 96*_volumeSlCh)
        self._volumeSrCh= math.floor(-96+ 96*_volumeSrCh)
        self._volumeCCh= math.floor(-96+ 96*_volumeCCh)
        self._volumeSwCh= math.floor(-96+ 96*_volumeSwCh)
        self.updateDevice()

if __name__ == "__main__":
    print("Start Test")
    testDev=m62446AFP()
    testDev.setVolume(-50,-90)
    testDev.setSurroundVolume(-100,-95)
    testDev.setCenterVolume(-10)
    testDev.setSubwooferVolume(-10)
    testDev.setOutput(1,1)
    testDev.setTleble(-2)
    testDev.setBase(6)
    testDev.updateDevice()
    print("Raw set done")
    testDev.setMasterVolume(0.9)
    testDev.setBalanceFront(0.6)
    testDev.updateRelativeVolume()
    print("End Test")

# gpioLatch = gpiozero.OutputDevice(17)
# gpioClock = gpiozero.OutputDevice(27)
# gpioData  = gpiozero.OutputDevice(22)

# gpioLatch.off()
# gpioClock.off()
# gpioData.off()


# def sendWord(word):
#     global gpioLatch
#     global gpioClock
#     global gpioData
#     print("send")
#     gpioLatch.on()
#     usleep = lambda x: time.sleep(x/1000000.0)
#     usleep(50)
#     gpioLatch.off()
#     usleep(50)
#     for i in range(0,16):
#         if(word&1<<i):
#             print("1",end='')
#             gpioData.on()
#             usleep(50)
#             gpioClock.on()
#             usleep(50)
#             gpioClock.off()
#             usleep(50)
#             gpioData.off()
#         else:
#             print("0",end='')
#             gpioData.off()
#             usleep(50)
#             gpioClock.on()
#             usleep(50)
#             gpioClock.off()
#             usleep(50)
#             gpioData.off()
#     gpioLatch.on()
#     usleep(50)
#     gpioLatch.off()
#     print("\n send done")

# print("Put volume")
# vol =int('0b1000010000001000',2);
# sendWord(vol)
# vol =int('0b1100010000001000',2);
# sendWord(vol)
# vol =int('0b0100010000001000',2);
# sendWord(vol)




# print("Change Outputport")
# vol =int('0b0000010001100100',2);
# sendWord(vol)


#gpioData.on()
#time.sleep(220)

