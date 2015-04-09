import socket
import threading
import time

class server():

    def __init__(self,port):
        host = socket.gethostbyname('localhost')
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, self.port))
        self.sock.listen(1)

        print 'waiting for connection...'

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

    def doCommand(self,header):
        if header == 'poll':
            self.sendResponse(""
                + 'analogRead/a0 1' + chr(10)
                + 'analogRead/a1 0' + chr(10)
                + 'digitalRead/d0 false' + chr(10)
                )
        elif header == 'reset_all':
                #moControl.getArduino().resetAll();
                print "reset_all"
                self.sendResponse("ok")
        else:
            las = header.split("/")
            if las[0] == 'digitalWrite':
                print las[1]
                print las[2]
                #moControl.getArduino().digitalWrite(las[1], las[2])
            elif las[0] == 'analogWrite':
                print las[1]
                print las[2]
                #moControl.getArduino().analogWrite(las[1], Double.valueOf(las[2]).intValue())
            else:
                print "else1"
                self.sendResponse("ok")

    def doHelp(self):
        # Optional: return a list of commands understood by this server
        help = "Server HTTP Extension BlocklyDuino<br><br>";
        self.sendResponse(help)

    def main(self):
        print "main started"
        thread = threading.Thread(target=self.readSocket)
        thread.setDaemon(True)
        thread.start()

    def readSocket(self):
        while True:
            (self.client_sock, self.client_addr) = self.sock.accept()

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
        self.client_sock.close()
        self.sock.close()

if __name__ == "__main__":
    server = server(8099)
    server.main()

    while True:
        try:
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
             break
        except:
            print "error"
            break

server.close()
