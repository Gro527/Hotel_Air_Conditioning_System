## 对应角色：前台
from Hotel_Air_Conditioning_System.impl import Invoice
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
from Hotel_Air_Conditioning_System.impl import Service
import json

class CreateInvoiceController(object):
    def CreateInvoice(self, room_id, date_out):
        # 先获取详单
        s=Service.Service()
        rdrList,total,date_in = s.ShowDetailBill(room_id)

        #invoice = Invoice.Invoice(room_id, date_in, date_out)
        #idao = iInvoiceDAO()
        #total = idao.GetTotal(room_id,date_out)
        # ???
        return json.dumps({'dateIn':date_in,'dateOut':date_out,'total':total})

cic = CreateInvoiceController()