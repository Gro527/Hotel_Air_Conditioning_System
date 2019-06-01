## 对应角色：经理
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
from Hotel_Air_Conditioning_System.dao.iRecordDAO import iRecordDAO
import datetime
import json
from flask import current_app
class ReporterController(object):
    def QueryReport(self, type_report, until):
        res = []
        start_date = datetime.date.today()
        if type_report == "D":
            start_date = until - datetime.timedelta(days=1)
        elif type_report == "W":
            start_date = until - datetime.timedelta(days=7)
        elif type_report == "M":
            start_date = until - datetime.timedelta(days=30)
        elif type_report == "A":
            start_date = until - datetime.timedelta(days=365)
        iidao = iInvoiceDAO()
        irdao = iRecordDAO()
        inv_list = iidao.GetInvoiceByDate(start_date, until)
        room_list = {}
        for inv in inv_list:
            room = room_list.get(inv.room_id,{})
            if not room:
                room["roomID"] = inv.room_id
                room["swh"] = 0
                room["time"] = datetime.timedelta(seconds=0)
                room["sch"] = 0
                room["rdr"] = 0
                room["chgTmp"] = 0
                room["chgSpd"] = 0
                room["total"] = 0
            rec_list = irdao.GetRecord(inv.id)
            on = False
            dur = datetime.timedelta(seconds=0)
            num = 0
            act_time = datetime.datetime.now()
            last_feerate = 0
            for rec in rec_list:
                # 不是第一条记录
                if num != 0:
                    dur = rec.start_time - act_time
                if on == True:
                    room["time"] += dur
                if rec.action_type == "on":
                    if on == True:
                        room["sch"] += 1
                    else:
                        on = True
                        room["swh"] += 1
                elif rec.action_type == ("hold" or "wait"):
                    room["swh"] += 1
                elif rec.action_type == "off":
                    on = False
                    room["sch"] += 1
                elif rec.action_type == "change_temp":
                    room["chgTmp"] += 1
                elif rec.action_type == "change_speed":
                    room["chgSpd"] += 1
                room["rdr"] += 1
                room["total"] += last_feerate * dur.seconds
                last_feerate = rec.fee_rate
                act_time = rec.start_time
                num += 1
            room_list[inv.room_id] = room
        for room in room_list:
            room_list[room]["time"] = str(room_list[room]["time"])
            res.append(room_list[room])
            
        ## 保存报告
        jsontxt = json.dumps(res)
        base_fname = "rep_"+type_report+"_"+until.strftime('%Y-%m-%d')
        f = open(current_app.root_path+"\\rep\\"+base_fname+"_json.txt","w")
        f.write(jsontxt)
        return jsontxt
    def PrintReport(self, report_id, date):
        pass


