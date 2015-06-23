# coding=utf-8

import serial
import time
import threading

class arduino():

    def __init__(self):
        self.ser = serial.Serial()
        self.dp_out = [-1] * 3   #d10,d11,d13
        self.dp_in = [-1] * 3    #d2,d3,d4
        self.ap = [-1] * 7   #A0,A1,A2,A3,A4,A5,A6
        self.cap_in = [-1]*12  #caps sensor
        self.oflg = 0

    def open(self,port,baudrate):
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.timeout = 1
        try:
            self.ser.open()
        except:
            return False
        self.oflg = 1
        time.sleep(1)
        return True

    def checkOpenflg(self):
        return self.oflg

    def main(self):
        #print u"Arduino started"
        self.stop_event = threading.Event() #スレッドを停止させるフラグ
        self.thread = threading.Thread(target=self.readStatus)
        self.thread.setDaemon(True)
        self.thread.start()

    def readStatus(self):
        while not self.stop_event.is_set():
            try:
                line = self.ser.readline().rstrip('\r\n')
            except:
                self.close()
            #print len(line)
            if len(line) > 0:
                #read state of digital Pin
                if line.find('D') != -1:
                    index = line.find('D')
                    dstr = line[index+1:index+4]
                    for x in range(0,3):
                        self.dp_in[x] = dstr[x]
                #read value of analog pin
                if line.find('A') != -1:
                    self.ap = line[line.find('A')+1:].split(',')
                #read value of Capactive Sensor MPR121
                if line.find('C') != -1:
                    index = line.find('C')
                    dstr = line[index+1:index+13]
                    for x in range(0,12):
                        self.cap_in[x] = dstr[x]
            else:
                self.close()

    def getDigitalState(self):
        return self.dp_in

    def getAnalogState(self):
        return self.ap

    def getCapState(self):
        return self.cap_in

    def sendCommand(self,command,pin,val):
        msg = ""
        msg += str(pin) + command + str(val) + '\r\n'
        self.ser.write(msg)

    def close(self):
        #print u"port close()"
        if self.oflg == 1:
            self.oflg = 0
            self.stop_event.set()
            self.ser.close()

if __name__ == "__main__":
    ser = arduino()
#    ser.open("COM26",115200)
    ser.open("/dev/cu.usbmodem411",115200)
#    ser.open("/dev/cu.usbserial-A901OFEZ",115200)
    ser.main()

    while True:
        try:
            ser.sendCommand("D",13,0)
            time.sleep(5)
            ser.sendCommand("D",13,1)
            time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
             break
        except:
            #print "error"
            break

    ser.close()
    #print "stop"
