from datetime import datetime
class Wait_Queue_Item(object):
    def __init__(self, room_id, speed):
        self.room_id = room_id
        self.speed = speed
        self.start_time = datetime.now()
