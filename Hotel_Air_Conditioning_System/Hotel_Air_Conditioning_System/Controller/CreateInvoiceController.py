## 对应角色：前台
from Hotel_Air_Conditioning_System.impl import Invoice
from Hotel_Air_Conditioning_System.dao import iInvoiceDAO
import json

class CreateInvoiceController(object):
    def CreateInvoice(self, room_id, date_in, date_out):
        invoice = Invoice.Invoice(room_id, date_in, date_out)
        idao = iInvoiceDAO.iInvoiceDAO()
        total = idao.GetTotal(room_id,date_in,date_out)

cic = CreateInvoiceController()