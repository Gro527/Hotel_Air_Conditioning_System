from Hotel_Air_Conditioning_System.impl import gDict
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
from Hotel_Air_Conditioning_System.impl.Service import Service
class CheckStateHandler(object):
    def CheckRoomState(self, room_id):
        res ={}
        # 查看是否有客户入住，若存在订单且订单的date_out为空，则有客
        iidao = iInvoiceDAO()
        res["id"] = room_id
        res["ocp"] = "f"
        iiid = iidao.GetLastInvoiceId(room_id)
        if iiid != None:
            if iidao.GetInvoiceById(iiid).date_out == None:
                res["ocp"] = "t"
        # 当前空调状态
        res["state"] = "F"
        if res["ocp"] != "f":
            room = gDict["rooms"].get_room(room_id)
            res["state"] = room.state
            if res["state"] == "R":
                # 用服务对象来获取当前温度和风速
                serv = gDict["serv_pool"].serv_list[gDict["schedule"].SearchServing(room_id)]
                res["curTmp"] = serv.GetCurTmp()
                res["spd"] = serv.GetCurSpd()
            res["trgTmp"] = room.trg_tmp
        # 新建一个临时服务对象，计算当前用户累计消费
        res["total"] = Service(6666).ShowBill(iiid)
        return res

