#! /bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import m62446AFP as m
hostName = "PiMusic"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    dev =m.m62446AFP()
    def do_GET(self):
        splitPath = self.path.split('/')
        print('Path :')
        print(splitPath[0:-1],end='')
        para=splitPath[-1].split('?')
        print(para[0])
        if (para[0].lower()=='volume'):
            para=para[1]
            para = para.split('&')
            for item in para:
                s=item.split('=')
                print('Name: {}  , Value {} '.format(s[0],s[1] ))
                if(s[0].lower()=='master'):
                    self.dev.setMasterVolume(float(s[1]))
                elif(s[0].lower()=='balancefront'):
                    self.dev.setBalanceFront(float(s[1]))
                elif(s[0].lower()=='balanceback'):
                    self.dev.setBalanceBack(float(s[1]))
                elif(s[0].lower()=='balancefronttoback'):
                    self.dev.setBalanceFrontToBack(float(s[1]))
                elif(s[0].lower()=='balancecenter'):
                    self.dev.setBalanceCenter(float(s[1]))
                elif(s[0].lower()=='balancesubwoofer'):
                    self.dev.setBalanceSubwoofer(float(s[1]))
                else:
                    print("Unknown option: {}".format(s[0]))
             
        elif (para[0].lower()=='output'):
            para=para[1]
            para = para.split('&')
            id=-1
            value=-1
            for item in para:
                s=item.split('=')
                print('Name: {}  , Value {} '.format(s[0],s[1] ))
                if(s[0].lower()=='id'):
                    id=int(s[1])
                elif(s[0].lower()=='value'):
                    value=int(s[1])
            if(id>0) &(id<5) &(value>-1):
                self.dev.setOutput(id, value )
            
        else :
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            return 
        self.dev.updateRelativeVolume()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>M62446AFP API</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is the API to control the M62446AFP</p>", "utf-8"))
        self.wfile.write(bytes("<p>The route 'volume can be used to control the volume'</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")