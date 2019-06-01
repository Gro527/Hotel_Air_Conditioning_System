from Hotel_Air_Conditioning_System.impl import gDict
from Hotel_Air_Conditioning_System.dao import iInvoiceDAO
from Hotel_Air_Conditioning_System.dao import iRecordDAO
from datetime import datetime,date
class Service(object):
    def __init__(self, service_id):
        self.service_id = service_id
        self.is_working = False
        self.room_id = 0
        self.speed = 0
        self.trg_tmp = 0
        print("服务对象",service_id,"已创建")

    # 设置目标温度
    def SetTemp(self, temp):
        self.trg_tmp = temp
        gDict["rooms"].get_room(self.room_id).set_trgTmp(temp)
    def ShowBill(self, invoice_id):
        iidao = iInvoiceDAO.iInvoiceDAO()
        irdao = iRecordDAO.iRecordDAO()
        rec_list = irdao.GetRecord(invoice_id)
        num = 0
        total_price = 0
        current_f_r = 0
        time_s = datetime.now()
        for rec in rec_list:
            if(num == 0):   # 第一条记录
                time_s = rec.start_time
                current_f_r = rec.fee_rate
            else:
                duration = (rec.start_time - time_s).seconds
                total_price = total_price + (duration * current_f_r)
                time_s = rec.start_time
                current_f_r = rec.fee_rate
            num = num + 1
        # 查价格时空调仍在运行
        if current_f_r != 0:
            total_price += (datetime.now() - time_s).seconds * current_f_r
        return total_price

    # 生成rdrList并计算总价
    def ShowDetailBill(self,room_id):
        iidao = iInvoiceDAO.iInvoiceDAO()
        invoice_id = iidao.GetLastInvoiceId(room_id)    # 获取invoice_id
        invoice = iidao.GetInvoiceById(invoice_id)
        date_out =  invoice.date_out
        date_in = invoice.date_in          # 获取date_in
        irdao = iRecordDAO.iRecordDAO()
        ret = irdao.GetRecord(invoice_id)   # 获取详单记录
        if len(ret) == 0:
            return [],0,date_in
        # 若详单最后一条记录不为off，则此时off
        if ret[-1].action_type != "off":
            print("111")
            gDict["schedule"].OnRequest(room_id, {"req_type":"off"})
            if ret[-1].action_type != "off":
                print("222")
                irdao.AddRecord(room_id, "0",  "off")
        # 若无date_out，写dateout
        if date_out == None:
            date_out = datetime.now().replace(microsecond=0)
            iidao.SetDateOut(invoice_id, date_out)
        rdrlist = []              # 初始化rdrlist
        total_price = 0           # 初始化总价
        num = 0
        while num < len(ret):
            # 将该条记录添加进rdrList
            ## 格式待改
            rdrlist.append({'time':str(ret[num].start_time),'rate':ret[num].fee_rate,'spd':ret[num].speed})
            # 价钱累积
            if(num == 0):   # 第一条记录
                time_s = ret[num].start_time
                current_f_r = ret[num].fee_rate
            else:
                duration = (ret[num].start_time - time_s).seconds
                total_price = total_price + (duration * current_f_r)
                time_s = ret[num].start_time
                current_f_r = ret[num].fee_rate
            num = num + 1

        iidao.SetTotal(invoice_id, total_price)
        return rdrlist,total_price,date_in,date_out, invoice_id

    def ShowReport(self):
        pass
    def SetState(self, state):
        self.state = state

    # 绑定房间
    def BindRoom(self, room_id, speed):
        self.room_id = room_id
        self.is_working = True
        room = gDict["rooms"].get_room(room_id)
        if room == None:
            self.trg_tmp = gDict["settings"].get("default_targetTemp", 24)
            gDict["rooms"].new_room(room_id, self.trg_tmp)
        else:
            self.trg_tmp = room.trg_tmp
        self.speed = speed
        

    # 更改风速
    def SpdChange(self, speed):
        self.speed = speed
    
    # 释放服务
    def ReleaseRoom(self):
        self.room_id = 0
        self.is_working = False
        self.speed = 0
        self.trg_tmp = 0
    
    # 获取当前温度
    def GetCurTmp(self):
        room = gDict["rooms"].get_room(self.room_id)
        if room == None:
            return None
        # 计算温度，每工作1秒改变温度0.01度
        if self.is_working == True:
            sche = gDict["schedule"]
            if gDict["settings"].get("mode") == "C":
                curtmp = room.tmp_dec((datetime.now() - room.last_op_time).seconds * 0.01)
                # 当温度低于目标温度时，暂停服务进入等待序列
                if curtmp < self.trg_tmp:
                    print("hahahaha")
                    room.set_state("H")
                    iRecordDAO.iRecordDAO().AddRecord(self.room_id, self.speed, "hold")
                    waiting = sche.GetLongestWait()
                    sche.ReleaseService(self.service_id)
                    # 若等待队列不为空，则等待队列中等待时间最长的目标开始服务
                    if waiting != None:
                        sche.NewService(waiting.room_id, waiting.speed)
                return curtmp
            else:
                curtmp = room.tmp_up((datetime.now() - room.last_op_time).seconds * 0.01)
                # 当温度高于目标温度时，暂停服务进入等待序列
                if curtmp > self.trg_tmp:
                    room.set_state("H")
                    iRecordDAO.iRecordDAO().AddRecord(self.room_id, self.speed, "hold")
                    waiting = sche.GetLongestWait()
                    sche.ReleaseService(self.service_id)
                    if waiting != None:
                        sche.NewService(waiting.room_id, waiting.speed)
                return curtmp
        else:
            return room.ref_tmp()
    
    # 获取目标温度
    def GetTrgTmp(self):
        return self.trg_tmp

    # 获取当前风速
    def GetCurSpd(self):
        return self.speed
