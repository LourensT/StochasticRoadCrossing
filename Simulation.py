from Distribution import Distribution
from FES import FES
from Event import Event
from SimulationResults import SimulationResults

from scipy import stats
from collections import deque
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


class Car:

    def __init__(self, arrTime):
        self.arrTime = arrTime

class Simulation:

    def __init__(self, s, m, h):
        #init simulations
        self.mainArrDist = Distribution(stats.expon(scale=1/m))
        self.sideArrDist = Distribution(stats.expon(scale=1/s))

        self.s = s
        self.m = m
        self.h = h

    def simulate(self, T, verbose=False):
        #start simulation untill time reaches T

        fes = FES()
        simres = SimulationResults(self.s, self.m, self.h, T)
        
        queue = deque()
        t = 0

        #schedule first arrival
        c0 = Car(self.sideArrDist.rvs())
        fes.add(Event(c0.arrTime, Event.ARRIVAL, car=c0))

        #schedule first departure
        fes.add( Event(self.mainArrDist.rvs(), Event.GAP))

        while t < T:
            if verbose:
                print(fes.getTypesList(), fes.events)
            
            e = fes.next()
            simres.registerQueue(t, len(queue))

            
            if e.type == Event.GAP:
                #depart the right amount of cars from the queue
                duration = e.time - t
                departures = int(duration // self.h)
                
                for _ in range(departures):
                    #a car leaves the queue, we save their waitingtime
                    if len(queue) != 0:
                        c = queue.popleft()                    
                        simres.registerWaitingTime(t - c.arrTime) 

                # TODO WHERE TO SET TIME 
                t = e.time

                # schedule next gap
                fes.add( Event(t+self.mainArrDist.rvs(), Event.GAP) )

            if e.type == Event.ARRIVAL:
                #add car to the queue
                t = e.time
                queue.append(e.car)

                #schedule next car 
                c1 = Car(t + self.sideArrDist.rvs())
                fes.add(Event(c1.arrTime,Event.ARRIVAL, car=c1))


        return simres

if __name__ == "__main__":
    nrRuns = 1000
    waitingtimes = np.zeros(nrRuns)
    queuelengths = np.zeros(nrRuns)

    for i in range(nrRuns):
        sim = Simulation(0.25, 0.25, 1)
        sr = sim.simulate(300)

        waitingtimes[i] = sr.getMeanWaitingTime()
        queuelengths[i] = sr.getMeanQueuelength()

    print('waitingtimes')
    print(np.mean(waitingtimes), np.std(waitingtimes))
    print('queuelengths')
    print(np.mean(queuelengths), np.std(queuelengths))
    #sr.plotQueuelength()

