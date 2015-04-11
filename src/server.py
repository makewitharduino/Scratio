import socket
import threading
import time
from arduino import *

class server():

    def __init__(self,port):
        self.stop_event = threading.Event()
        host = socket.gethostbyname('localhost')
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, self.port))
        self.sock.listen(1)
        self.ser = arduino()

        #self.call_arduino("COM26")

        print 'waiting for connection...'

    def call_arduino(self,port):
        self.ser = arduino()
        self.ser.open(port,115200)
        self.ser.main()

    def sendResponse(self,s):
        crlf = '\r\n'
        msg = 'HTTP/1.1 200 OK' + crlf
        msg += 'Content-Type: text/html; charset=ISO-8859-1' + crlf
        msg += 'Access-Control-Allow-Origin: *' + crlf
        msg += crlf
        msg += s + crlf
        self.client_sock.send(msg)

    def htmlRequest(self,header):
        if  header.find('GET ') == -1:
            print 'Este servidor solo acepta conexiones HTTP GET'
            return
        i = header.find('HTTP/1')

        if i < 0:
            print 'Cabezera HTTP GET incorracta.'
            return

        header = header[5:i-1]

        if header == 'favicon.ico':
            return # igore browser favicon.ico requests
        elif header == 'crossdomain.xml':
            #self.sendPolicyFile();
            print "policy"
        elif len(header) == 0:
            self.doHelp();
        else:
            self.doCommand(header)

    def getState(self,state):
        if state != 0:
            return "true"
        else:
            return "false"

    def doCommand(self,header):
        if self.ser.checkOpenflg() == 0:
            return

        if header == 'poll':
            dp_in = self.ser.getDigitalState()
            ap = self.ser.getAnalogState()
            self.sendResponse(""
                + 'analogRead/a0 ' + str(ap[0]) + chr(10)
                + 'analogRead/a1 ' + str(ap[1]) + chr(10)
                + 'analogRead/a2 ' + str(ap[2]) + chr(10)
                + 'analogRead/a3 ' + str(ap[3]) + chr(10)
                + 'analogRead/a4 ' + str(ap[4]) + chr(10)
                + 'analogRead/a5 ' + str(ap[5]) + chr(10)
                + 'digitalRead/d2 ' + self.getState(dp_in[0])  + chr(10)
                + 'digitalRead/d4 ' + self.getState(dp_in[1])  + chr(10)
                + 'digitalRead/d7 ' + self.getState(dp_in[2])  + chr(10)
                + 'digitalRead/d8 ' + self.getState(dp_in[3])  + chr(10)
                + 'digitalRead/d12 ' + self.getState(dp_in[4])  + chr(10)
                + 'digitalRead/d13 ' + self.getState(dp_in[5])  + chr(10)
            )
        elif header == 'reset_all':
                #moControl.getArduino().resetAll();
                print "reset_all"
                self.sendResponse("ok")
        else:
            las = header.split("/")
            if las[0] == 'digitalWrite':
                pin = las[1][1:]
                state = 0
                if las[2] == "true":
                    state = 1
                self.ser.sendCommand("D",pin,state)
            elif las[0] == 'analogWrite':
                pin = las[1][1:]
                self.ser.sendCommand("A",pin,int(las[2]))
            elif las[0] == 'tone':
                pin = las[1][1:]
                self.ser.sendCommand("T",pin,int(las[2]))
            else:
                print "else1"
                self.sendResponse("ok")

    def doHelp(self):
        # Optional: return a list of commands understood by this server
        help = "Server HTTP Extension BlocklyDuino<br><br>";
        self.sendResponse(help)

    def main(self):
        print "main started"
        self.thread = threading.Thread(target=self.readSocket)
        self.thread.setDaemon(True)
        self.thread.start()

    def readSocket(self):
        while True:
            try:
                (self.client_sock, self.client_addr) = self.sock.accept()
            except socket.error:
                break
            msg = ''
            while msg.find('\n') == -1:
                msg = self.client_sock.recv(1024)
                if len(msg) < 0:
                    print "Socket closed; no HTTP header."
                    break
                msg += msg;

            self.htmlRequest(msg)
            self.client_sock.close()

    def close(self):
        print "server close()"
        self.ser.close()
        self.stop_event.set()
        #self.client_sock.close()
        self.sock.close()


if __name__ == "__main__":
    server = server(8099)
    server.main()
#    server.call_arduino("COM26")
    server.call_arduino("/dev/cu.usbmodem411")

    while True:
        try:
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
             break
        except:
            print "error"
            break

    #ser.close()
    server.close()
