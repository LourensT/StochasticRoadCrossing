class Event:
    """class for all arrival and departure events"""
    ARRIVAL = 0     #user arrives at network
    GAP  = 1  #user departs a server
    

    def __init__(self, t, eventType, car=None):
        self.type = eventType
        self.time = t
        self.car = car

    def __repr__(self):
        """for debugging purposes"""
        s = "Event "
        if self.type == Event.ARRIVAL:
            s += "Arrival"
        elif self.type == Event.GAP:
            s += "GAP"

        s += (", time: " + str(self.time))

        return s

    def __lt__(self, other):
        return self.time < other.time