import socket

host = socket.gethostbyname('localhost')
port = 8099

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)

print 'waiting for connection...'

def sendResponse(s):
    crlf = '\r\n'
    msg = 'HTTP/1.1 200 OK' + crlf
    msg += 'Content-Type: text/html; charset=ISO-8859-1' + crlf
    msg += 'Access-Control-Allow-Origin: *' + crlf
    msg += crlf
    msg += s + crlf
    client_sock.send(msg)

def htmlRequest(header):
    if  header.find('GET ') == -1:
        print 'Este servidor solo acepta conexiones HTTP GET'
        return
    i = header.find('HTTP/1')

    if i < 0:
        print 'Cabezera HTTP GET incorracta.'
        return

    header = header[i-5:i-1]

    print header
    if header == 'favicon.ico':
        return # igore browser favicon.ico requests
    elif header == 'crossdomain.xml':
        #sendPolicyFile();
        print 'sendPolicyFile'
    elif len(header) == 0:
        #doHelp();
        print 'doHelp'
    else:
        doCommand(header)

def doCommand(header):
    if header == 'poll':
        sendResponse(""
            + 'analogRead/a0 1' + chr(10)
            + 'analogRead/a1 0' + chr(10)
            + 'digitalRead/d0 false' + chr(10)
            )
    elif header == 'reset_all':
            #moControl.getArduino().resetAll();
            print "reset_all"
            sendResponse("ok")
    else:
        """
        String[] las = header.split("/")
        if las[0].equalsIgnoreCase("digitalWrite"):
            moControl.getArduino().digitalWrite(las[1], las[2])
        elif(las[0].equalsIgnoreCase("analogWrite"))
            moControl.getArduino().analogWrite(las[1], Double.valueOf(las[2]).intValue())
        else:
            System.out.println("Comando no procesado: " + header)
        """
        print "else"
        sendResponse("ok")

while True:
    (client_sock, client_addr) = sock.accept()
    print 'connection start'

    msg = ''
    while msg.find('\n') == -1:
        msg = client_sock.recv(1024)
        if len(msg) < 0:
            print "Socket closed; no HTTP header."
            break
        msg += msg;

    htmlRequest(msg)
    client_sock.close()

client_sock.close()
sock.close()
