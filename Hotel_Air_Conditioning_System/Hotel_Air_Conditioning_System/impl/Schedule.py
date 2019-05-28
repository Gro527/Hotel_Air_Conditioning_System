## 对应角色：管理员
from Hotel_Air_Conditioning_System.impl import gDict
class Schedule(object):
    max_service = 3
    def CreateServQueue(self):
        self.serv_queue = []
        print("服务队列已初始化")
    def CreateWaitQueue(self):
        self.wait_queue = []
        print("等待队列已初始化")
    def SetState(self, State):
        pass
    # 添加服务
    def NewService(self):
        pass
    # 添加到等待队列
    def NewWaiting(self):
        pass
    # 释放服务添加到等待队列（需计算此次服务的费用）
    def ReleaseService(self, service_id):
        pass
    # 释放服务不添加到等待队列
    def TerminateService(self, service_id):
        pass
    # 从等待队列中删除
    def TerminateWaiting(self, room_id):
        pass

    # 在服务队列中查找房间号
    def SearchServing(self, room_id):
        for obj in self.serv_queue:
            if obj.room_id == room_id:
                service = gDict["serv_pool"].serv_list[obj.service_id]
                return service.service_id
        return -1
    # 在等待队列中查找房间号
    def SearchWaiting(self, room_id):
        for obj in self.wait_queue:
            if obj.room_id == room_id:
                return True
        return False

    # 对请求进行调度
    def OnRequest(self, room_id, req_type):
        ## 当前房间正在服务
        for serv in self.serv_queue:
            if serv.room_id == room_id:
                if req_type == 'on':
                    return {"state":"OK"}
                ##待添加
        ## 当前房间未在服务，且在等待队列中    
        for req in self.wait_queue:
            if req.room_id == room_id:
                if req_type == 'on':
                    return {"state":"Waiting"}
        ## 当前房间未在服务，且有空余服务对象资源
        if len(self.serv_queue) < self.max_service:
            pass
    def __init__(self):
        print("调度对象已创建")
        self.CreateServQueue()
        self.CreateWaitQueue()

