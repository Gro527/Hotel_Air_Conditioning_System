## 对应角色：前台
from Hotel_Air_Conditioning_System.controller import *  

class CreateInvoiceController(object):
    def CreateInvoice(self, room_id, date_in, date_out):
        invoice = Invoice.Invoice(room_id, date_in, date_out)
        dao = iInvoiceDAO.iInvoiceDAO()
        dao.sess.add(invoice)
        dao.sess.commit()

cic = CreateInvoiceController()