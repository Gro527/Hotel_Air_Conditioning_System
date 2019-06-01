## 对应角色：管理员
from Hotel_Air_Conditioning_System.impl import gDict
from Hotel_Air_Conditioning_System.impl.Serv_Queue_Item import Serv_Queue_Item
from Hotel_Air_Conditioning_System.impl.Wait_Queue_Item import Wait_Queue_Item
import operator
from flask_apscheduler import APScheduler
from flask import current_app
from datetime import datetime,timedelta
from Hotel_Air_Conditioning_System import app
from Hotel_Air_Conditioning_System.dao.iRecordDAO import iRecordDAO
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO

# 时间片到，执行调度
def Timeout(room_id):
    print(room_id+': timeout')
    sche = gDict["schedule"]
    wait = sche.SearchWaiting(room_id)
    # 若有空闲服务，直接开始服务
    if len(sche.serv_queue) < sche.max_service:
        sche.WaitingToServing(room_id)
        iRecordDAO().AddRecord(room_id, wait.speed, "on")
        return
    # 若无空闲服务
    # 当前房间风速需至少大于等于一个正在服务的房间风速，才能进入服务队列
    # wait = sche.SearchWaiting(room_id)
    # if wait == None:
    #     return
    least_service_id = sche.GetLeastPriorService()
    if wait.priority >= sche.GetSpeed(least_service_id)[1]:
        iRecordDAO().AddRecord(sche.GetRoomId(least_service_id), sche.GetSpeed(least_service_id)[0], "wait")
        sche.ReleaseService(least_service_id)
        sche.WaitingToServing(room_id)
        iRecordDAO().AddRecord(room_id, wait.speed, "on")

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


    ## 服务和队列操作
    # 添加服务
    def NewService(self, room_id, speed):
        if gDict["serv_pool"].state != "ready":
            print("服务对象未就绪")
            return
        if len(self.serv_queue) == self.max_service:
            print("服务对象资源已满")
            return 
        for serv in gDict["serv_pool"].serv_list:
            if serv.is_working == False:
                self.serv_queue.append(Serv_Queue_Item(room_id, serv.service_id, speed))
                serv.BindRoom(room_id, speed)
                ## 更改房间状态
                gDict["rooms"].get_room(room_id).set_state("R")
                break
    # 从等待队列开始服务
    def WaitingToServing(self, room_id):
        wait_item = self.SearchWaiting(room_id)
        if wait_item == None:
            print("错误！当前房间未处于等待队列！")
            return
        if len(self.serv_queue) == self.max_service:
            print("服务对象资源已满")
            return 
        for serv in gDict["serv_pool"].serv_list:
            if serv.is_working == False:
                self.serv_queue.append(Serv_Queue_Item(room_id, serv.service_id, wait_item.speed))
                serv.BindRoom(room_id, wait_item.speed)
                ## 更改房间状态
                gDict["rooms"].get_room(room_id).set_state("R")
                self.wait_queue.remove(wait_item)
                break
    # 添加到等待队列
    def NewWaiting(self, room_id, speed):
        self.wait_queue.append(Wait_Queue_Item(room_id, speed))
        # 添加到定时任务中
        job = {
            "id" : room_id,
            "func" : 'Timeout'
        }
        result = app.apscheduler.add_job(func=__name__+':'+job['func'], id=job['id'], next_run_time= datetime.now()+timedelta(seconds=5),args=[room_id])
        print(result)
        
        gDict["rooms"].get_room(room_id).set_state("W")
        return {"state":"waiting"}
    # 释放服务添加到等待队列
    def ReleaseService(self, service_id):
        gDict["serv_pool"].serv_list[service_id].ReleaseRoom()
        for serv in self.serv_queue:
            if serv.service_id == service_id:
                speed = serv.speed
                room_id = serv.room_id
                self.serv_queue.remove(serv)
                self.NewWaiting(room_id, speed)
                gDict["rooms"].get_room(room_id).set_state("H")
                break
    # 释放服务不添加到等待队列（需在数据库中记录一条off操作）
    def TerminateService(self, service_id):
        ## 数据库操作！！！！！
        gDict["serv_pool"].serv_list[service_id].ReleaseRoom()
        for serv in self.serv_queue:
            if serv.service_id == service_id:
                self.serv_queue.remove(serv)
                gDict["rooms"].get_room(serv.room_id).set_state("F")
                break
    # 从等待队列中删除(需在数据库中记录一条off操作)
    def TerminateWaiting(self, room_id):
        ## 数据库操作！！！！！
        wait_item = self.SearchWaiting(room_id)
        if wait_item != None:
            self.wait_queue.remove(wait_item)
            gDict["rooms"].get_room(room_id).set_state("R")

    ## 查找操作
    # 根据服务号查风速
    def GetSpeed(self, service_id):
        for obj in self.serv_queue:
            if obj.service_id == service_id:
                return obj.speed, obj.priority

    # 根据服务号查房间号
    def GetRoomId(self, service_id):
        for obj in self.serv_queue:
            if obj.service_id == service_id:
                return obj.room_id

    # 在服务队列中根据房间号查找服务号
    def SearchServing(self, room_id):
        for obj in self.serv_queue:
            if obj.room_id == room_id:
                service = gDict["serv_pool"].serv_list[obj.service_id]
                return service.service_id
        return None

    # 在等待队列中查找房间号是否存在
    def SearchWaiting(self, room_id):
        for obj in self.wait_queue:
            if obj.room_id == room_id:
                return obj
        return None

    # 查找服务优先级最低的服务
    def GetLeastPriorService(self):
        if len(self.serv_queue) == 0:
            return None
        ## 根据风速优先级排序
        self.serv_queue.sort(key = operator.attrgetter('priority'))
        least_priorty = self.serv_queue[0].priority
        least_priorty_list = []
        for serv in self.serv_queue:
            if serv.priority == least_priorty:
                least_priorty_list.append(serv)
        ## 在风速最低的服务中根据服务开始时间排序
        least_priorty_list.sort(key = operator.attrgetter('start_time'))
        return least_priorty_list[0].service_id

    # 查找等待队列中等待最久的目标
    def GetLongestWait(self):
        if len(self.wait_queue) == 0:
            return None
        self.wait_queue.sort(key = operator.attrgetter('start_time'))
        return self.wait_queue[0]



    ## 核心模块
    # 对请求进行调度
    def OnRequest(self, room_id, req):
        req_type = req.get("req_type", 0)
        trg = req.get("trg", 0)
        ## 当前房间正在服务
        for serv in self.serv_queue:
            if serv.room_id == room_id:
                if req_type == 'on':
                    return {"state":"OK"}
                elif req_type == 'off':
                    self.TerminateService(serv.service_id)
                    iRecordDAO().AddRecord(room_id, serv.speed, "off")
                    return {"state":"OK"}
                elif req_type == 'tmp':
                    gDict["serv_pool"].serv_list[serv.service_id].SetTemp(trg)
                    iRecordDAO().AddRecord(room_id, serv.speed, "change_temp")
                    return {"state":"OK"}
                elif req_type == 'spd':
                    gDict["serv_pool"].serv_list[serv.service_id].SpdChange(trg)
                    serv.SetSpeed(trg)
                    iRecordDAO().AddRecord(room_id, serv.speed, "change_speed")
                    return {"state":"OK"}
        ## 当前房间未在服务，且在等待队列中    
        for req in self.wait_queue:
            if req.room_id == room_id:
                if req_type == 'on':
                    return {"state":"Waiting"}
                elif req_type == 'off':
                    self.TerminateWaiting(room_id)
                    iRecordDAO().AddRecord(room_id, req.speed, "off")
                    return {"state":"OK"}
                elif req_type == 'tmp':
                    gDict["rooms"].get_room(room_id).set_trgTmp(trg)
                    iRecordDAO().AddRecord(room_id, req.speed, "change_temp")
                    return {"state":"OK"}
                elif req_type == 'spd':
                    req.SetSpeed(trg)
                    ## 取代优先级最低的当前服务
                    least = self.GetLeastPriorService()
                    if least != None:
                        if self.GetSpeed(least)[1] < req.priority:
                            self.ReleaseService(least)
                            iRecordDAO().AddRecord(least.room_id, least.speed, "wait")
                            self.WaitingToServing(req.room_id)
                            iRecordDAO().AddRecord(room_id, trg, "change_speed")
                            iRecordDAO().AddRecord(room_id, trg, "on")
                            return {"state":"OK"}
                        else:
                            iRecordDAO().AddRecord(room_id, trg, "change_speed")
                            return {"state":"Waiting"}
        ## 当前房间未在服务,未在等待，且有空余服务对象资源
        if len(self.serv_queue) < self.max_service:
            if req_type == 'on':
                # 若无Invoice记录，则视为一次订房
                iInvoiceDAO().AddInvoice(room_id)
                ### 暂定开机默认风速为M，若策略有改变，请更改此处！！！
                self.NewService(room_id, 'M')
                iRecordDAO().AddRecord(room_id,"M","on")
                return {"state":"OK"}
            elif req_type == 'off':
                return {"state":"OK"}
            elif req_type == 'tmp':
                return {"state":"Invalid"}
            elif req_type == 'spd':
                return {"state":"Invalid"}
        ## 当前房间未在服务，未在等待，且无空余服务对象资源
        else:
            if req_type == 'on':
                iInvoiceDAO().AddInvoice(room_id)
                # 找出优先级最低的服务，若当前服务优先级高于其，则取而代之，反之加入等待队列
                least = self.GetLeastPriorService()
                if self.GetSpeed(least)[1] < 2:
                    print("房间号：",least.room_id,"优先级过低，进入等待")
                    iRecordDAO().AddRecord(least.room_id, least.speed, "wait")
                    self.ReleaseService(least)
                    self.NewService(room_id, 'M')
                    iRecordDAO().AddRecord(room_id, "M", "on")
                    return {"state":"OK"}
                else:
                    gDict["rooms"].new_room(room_id, gDict["settings"].get("default_targetTemp",24))
                    self.NewWaiting(room_id, 'M')
                    iRecordDAO().AddRecord(room_id, 'M', "wait")
                    return {"state":"Waiting"}
            elif req_type == 'off':
                return {"state":"OK"}
            elif req_type == 'tmp':
                return {"state":"Invalid"}
            elif req_type == 'spd':
                return {"state":"Invalid"}



    def __init__(self):
        print("调度对象已创建")
        self.CreateServQueue()
        self.CreateWaitQueue()
        self.scheduler = APScheduler()


