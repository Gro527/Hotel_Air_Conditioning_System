## 对应角色：前台
from Hotel_Air_Conditioning_System.controller.CreateInvoiceController import CreateInvoiceController
from Hotel_Air_Conditioning_System.impl import Service
from Hotel_Air_Conditioning_System.dao.iInvoiceDAO import iInvoiceDAO
import json
import os
from flask import current_app

class CreateRDRController(object):
    def CreateRDR(self, room_id):
        iidao = iInvoiceDAO()
        date_in = iidao.GetInvoiceById(iidao.GetLastInvoiceId(room_id)).date_in
        base_fname = "rdr_"+str(room_id)+"_"+str(date_in)
        if os.path.exists("rdr/"+base_fname+"_json.json") == False:
            CreateInvoiceController().CreateInvoice(room_id)
        f = open(current_app.root_path+"\\rdr\\"+base_fname+"_json.json", "r")
        data = json.loads(f.read())
        date_in = data["date_in"]
        date_out = data["date_out"]
        rdrList = data["rList"]
        return json.dumps({'dateIn':str(date_in),'dateOut':str(date_out), 'rdrList':rdrList})

