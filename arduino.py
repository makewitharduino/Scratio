import serial
import time
import serial.tools.list_ports
import threading

class arduino():

    def __init__(self):
        self.ser = serial.Serial()
        self.dp_out = [0] * 6
        self.dp_in = [0] * 6
        self.ap = [0] * 5

    def getportlist(self):
        ports = []
        for x in lists:
            ports.append(x[0])

        print ports

    def open(self,port,baudrate):
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.timeout = 1
        self.ser.open()
        time.sleep(1)

    def main(self):
        print "main started"
        thread = threading.Thread(target=self.readStatus)
        thread.setDaemon(True)
        thread.start()

    def readStatus(self):
        while True:
            line = self.ser.readline().rstrip('\r\n')
            if len(line) > 0 and line.find('D') == 0:
                dstr = line[1:6]
                for x in range(0,5):
                    self.dp_in[x] = dstr[x]
                self.ap = line[line.find('A')+1:].split(',')

            time.sleep(1)

    def stop(self):
        self.stop_event.set()
        self.thread.join()

    def getDigitalState(self):
        return self.dp_in

    def getAnalogState(self):
        return self.ap

    def sendCommand(self,command,pin,val):
        msg = ""
        msg += str(pin) + command + str(val) + '\r\n'
        print msg
        self.ser.write(msg)

    def close(self):
        self.ser.close()

if __name__ == "__main__":
    ser = arduino()
#    ser.open("COM26",115200)
    ser.open("/dev/cu.usbmodem411",115200)
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
            print "error"
            break

    ser.close()
    print "stop"
