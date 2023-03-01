import bluetooth
#* 目标Server地址
bd_addr = "DC:A6:32:A4:E6:20"
class ClientSocket:
    def __init__(self, bd_addr, port=5):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((bd_addr, bluetooth.PORT_ANY))

    def send(self, msg):
        self.sock.send(msg)
        print(msg)

    def end(self):
        self.sock.close()
