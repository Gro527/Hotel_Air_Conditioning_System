## 对应角色：管理员
from Hotel_Air_Conditioning_System.impl.Service import Service
## self.state = {"init", "ready"}
class ServicePool(object):
    serv_list = []
    def CreateServ(self, serv_id):
        self.serv_list.append(Service(serv_id))
    def CreateSchedule(self):
        pass
    def __init__(self, max_service=3):
        self.max_service = max_service
        self.state ="init"
        print("服务对象池已创建")
        for i in range(max_service):
            self.CreateServ(i)
    def SetState(self,state):
        self.state = state
    def GetService(self, room_id):
        for serv in self.serv_list:
            if serv.room_id == room_id:
                return serv
        return None
        
