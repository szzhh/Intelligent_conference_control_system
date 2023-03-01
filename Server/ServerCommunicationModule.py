from bluetooth import *
class ServerSocket:
    def __init__(self, port=1):
        self.server_sock = BluetoothSocket(RFCOMM)
        self.server_sock.bind(('',22))
        port = self.server_sock.getsockname()[1]
        print(port)
        self.server_sock.listen(1)

    def active(self):
        client_sock, address = self.server_sock.accept()
        print ("Accepted connection from ",address)
        data = client_sock.recv(1024) 
        print ("received [%s]" % data)
        client_sock.close()
        return data
    
