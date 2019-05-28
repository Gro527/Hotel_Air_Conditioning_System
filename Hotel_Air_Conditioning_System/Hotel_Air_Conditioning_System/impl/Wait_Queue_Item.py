from datetime import datetime
class Wait_Queue_Item(object):
    def __init__(self, room_id, speed):
        self.room_id = room_id
        self.speed = speed
        if speed == 'L':
            self.priority = 1
        elif speed == 'M':
            self.priority = 2
        elif speed == 'H':
            self.priority = 3
        self.start_time = datetime.now()

    def SetSpeed(self, speed):
        self.speed = speed
        if speed == 'L':
            self.priority = 1
        elif speed == 'M':
            self.priority = 2
        elif speed == 'H':
            self.priority = 3