from ServerCommunicationModule import *
from ControlModule import *
bd_addr = 'DC:A6:32:A5:E6:20'
ss = ServerSocket()
EA = EventAction()
while True:
    print('连接成功')
    data = ss.active()
    print(data)
    data = str(data)[2:-1]
    print(data)
    action, params = data.split('#')[0], data.split('#')[1:]
    print(action)
    try:
        EA.response(action, para=params)
    except:
        pass
