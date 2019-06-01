## 对应角色：前台
from Hotel_Air_Conditioning_System.impl import Invoice,RDR
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
from Hotel_Air_Conditioning_System.impl import Service
import json
import random
import os
import datetime
from flask import current_app
class CreateInvoiceController(object):
    def CreateInvoice(self, room_id):
        iidao = iInvoiceDAO()
        invoice = iidao.GetInvoiceById(iidao.GetLastInvoiceId(room_id))
        date_in = invoice.date_in
        date_out = invoice.date_out
        # base_fname = "inv_"+str(room_id)+"_"+str(date_in)
        if not date_out:
            s = Service.Service(random.randint(1001,10001))
            res = s.ShowDetailBill(room_id)
            rdrlist = res[0]
            total = res[1]
            date_in = res[2]
            date_out = res[3]
            invoice_id = res[4]
            invoice = Invoice.Invoice(invoice_id, room_id, date_in, date_out, total)
            invoice.out_file()
            rdr = RDR.RDR(invoice_id, room_id, date_in, date_out, total, rdrlist)
            rdr.out_file()
        else:
            base_fname = "inv_"+str(room_id)+"_"+datetime.datetime.strftime(date_in,"%Y-%m-%d-%H%M%S")+"-"+datetime.datetime.strftime(date_out,"%Y-%m-%d-%H%M%S")
            f = open(current_app.root_path+"\\inv\\"+base_fname+"_json.txt","r")
            data = json.loads(f.read())
            date_in = data["date_in"]
            date_out = data["date_out"]
            total = data["total"]
        return json.dumps({'dateIn':str(date_in),'dateOut':str(date_out),'total':total})

cic = CreateInvoiceController()