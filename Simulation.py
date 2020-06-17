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

    def simulate(self, T, verbose=False, immediate_departure=False):
        #start simulation untill time reaches T

        fes = FES()
        simres = SimulationResults(self.s, self.m, self.h, T)
        
        queue = deque()
        t = 0
        prev_gap_time = 0

        #schedule first arrival
        c0 = Car(self.sideArrDist.rvs())
        fes.add(Event(c0.arrTime, Event.ARRIVAL, car=c0))

        #schedule first gap
        fes.add( Event(self.mainArrDist.rvs(), Event.GAP))

        simres.registerQueue(t, len(queue))

        while t < T:
            if verbose:
                print(fes.getTypesList(), fes.events)
            
            #next event
            e = fes.next()
            
            if e.type == Event.GAP:
                t = e.time
                #register the transitionprobability if there is no immediate_departure
                if not immediate_departure:
                    simres.registerQueue(t, len(queue))
                
                #depart the right amount of cars from the queue
                duration = e.time - prev_gap_time
                prev_gap_time = e.time
                departures = int(duration // self.h)
                
                for _ in range(departures):
                    #a car leaves the queue, we save their waitingtime
                    if len(queue) != 0:
                        c = queue.popleft()       

                #register the transitionprobability if there is immediate_departure
                if immediate_departure:
                    simres.registerQueue(t, len(queue))             

                # schedule next gap
                fes.add( Event(t+self.mainArrDist.rvs(), Event.GAP) )

            if e.type == Event.ARRIVAL:
                #add car to the queue
                t = e.time
                queue.append(e.car)

                #schedule next car 
                c1 = Car(t + self.sideArrDist.rvs())
                fes.add(Event(c1.arrTime,Event.ARRIVAL, car=c1))

        simres.registerQueue(t, len(queue))
        return simres

if __name__ == "__main__":
    timebound = 10000000 #since steady-state system we can run for extended time instead of monte-carlo

    sim = Simulation(0.515, 1.03, 1) #s, m, h
    sr = sim.simulate(timebound, immediate_departure=False)
    m = sr.getProbabilityMatrix(fp="load_9_case2.txt")
    np.set_printoptions(suppress=True)
    print(m)
    print([sum(m[i]) for i in range(10)])