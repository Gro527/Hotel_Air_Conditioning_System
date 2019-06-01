## 对应角色：前台
from Hotel_Air_Conditioning_System.Controller.CreateInvoiceController import CreateInvoiceController
from Hotel_Air_Conditioning_System.impl import Service
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
import json
import os
from flask import current_app
import datetime

class CreateRDRController(object):
    def CreateRDR(self, room_id):
        iidao = iInvoiceDAO()
        invoice = iidao.GetInvoiceById(iidao.GetLastInvoiceId(room_id))
        date_out = invoice.date_out
        if not date_out:
            CreateInvoiceController().CreateInvoice(room_id)
        invoice = iidao.GetInvoiceById(iidao.GetLastInvoiceId(room_id))
        date_in = invoice.date_in
        date_out = invoice.date_out
        base_fname = "rdr_"+str(room_id)+"_"+datetime.datetime.strftime(date_in,"%Y-%m-%d-%H%M%S")+"-"+datetime.datetime.strftime(date_out,"%Y-%m-%d-%H%M%S")
        f = open(current_app.root_path+"\\rdr\\"+base_fname+"_json.txt", "r")
        data = json.loads(f.read())
        date_in = data["date_in"]
        date_out = data["date_out"]
        rdrList = data["rList"]
        return json.dumps({'dateIn':str(date_in),'dateOut':str(date_out), 'rdrList':rdrList})

