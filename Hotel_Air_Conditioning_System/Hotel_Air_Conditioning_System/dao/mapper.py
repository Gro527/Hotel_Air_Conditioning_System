from Hotel_Air_Conditioning_System.dao import *
from Hotel_Air_Conditioning_System.dao.connector import *


def init_db():
    base.metadata.create_all(engine)

class iInvoice(base):
    __tablename__ = 'invoice'
    id = Column(Integer,
               Sequence('invoice_id_seq', start=1001, increment=1),
               primary_key = True)
    room_id = Column(String(16))
    date_in = Column(Date)
    date_out = Column(Date)
    total = Column(Float)



#class Action_Type(Enum):
#    request_on = 1
#    start = 2
#    change_temp = 3
#    change_speed = 4
#    off = 5
    



class iRecord(base):
    __tablename__ = 'record'
    id = Column(Integer,
                Sequence('record_', start=10001, increment=1),
               primary_key = True)
    invoice_id = Column(Integer, ForeignKey("invoice.id"))
    start_time = Column(DateTime)
    action_type = Column(Enum("request_on", "start", "change_temp", "change_speed", "off", name="action_type"))
    price = Column(Float)
    


Session = sessionmaker(bind = engine)
session = Session()

init_db()