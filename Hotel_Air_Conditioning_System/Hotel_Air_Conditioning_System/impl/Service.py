## state = {'init', 'serving', 'ready'}
class Service(object):
    def __init__(self, service_id):
        self.service_id = service_id
        self.is_working = False
        self.room_id = 0
        self.state = "init"
        print("服务对象",service_id,"已创建")
    def SetTemp(self, temp):
        pass
    def ShowBill(self):
        pass
    def ShowDetailBill(self):
        pass
    def ShowReport(self):
        pass
    def SetState(self, state):
        self.state = state
    def GetCurTmp(self):
        if self.state == 'serving':
            pass
        return 28
    def GetTrgTmp(self):
        pass

