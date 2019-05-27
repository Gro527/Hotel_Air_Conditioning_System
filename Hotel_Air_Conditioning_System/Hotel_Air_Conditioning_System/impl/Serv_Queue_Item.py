from datetime import datetime
class Serv_Queue_Item(object):
    def __init__(self, room_id, service_id, speed):
        self.room_id = room_id
        self.service_id = service_id
        self.speed = speed
        self.start_time = datetime.now()
    
