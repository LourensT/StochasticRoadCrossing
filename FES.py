import heapq

class FES:
    #future event set, automatically sorted with heapq
    def __init__(self):
        self.events = []

    def add(self, event):
        """add an event to the heap
        """
        heapq.heappush(self.events, event)

    def next(self):
        """fetch next event"""
        return heapq.heappop(self.events)

    def getTypesList(self):
        return [e.type for e in self.events]