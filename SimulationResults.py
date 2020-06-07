import numpy as np
from collections import deque
import matplotlib.pyplot as plt
import itertools
from datetime import datetime
import csv
import pickle

class SimulationResults:
    """used to store relevant datapoints during a simulation """
    def __init__(self, s, m, h, T):
        
        dt = datetime.now().strftime("%H-%M-%S")
        self.fp = "{}_s_{}_m_{}h_{}timebound_{}.csv".format(dt, s, m, h, T)

        #car metrics
        self.waitingtimes = deque()

        #queue metrics
        self.timestamps = deque()
        self.queuelengths = deque()

    def registerWaitingTime(self, time):
        """register the traveltime of the customers routed from A-B
        """
        self.waitingtimes.append(time)

    def registerQueue(self, t, ql):
        """register the state of the network at given timestamp
        """
        self.timestamps.append(t)
        self.queuelengths.append(ql)

    def getMeanQueuelength(self):
        """returns mean queuelength"""
        T = self.timestamps[-1]
        sumQL = 0

        for i in range(1, len(self.timestamps)):
            duration = self.timestamps[i] - self.timestamps[i-1]
            sumQL += duration*self.queuelengths[i]
        
        return sumQL/T

    def getMeanWaitingTime(self):
        """return mean waiting time of car"""
        return np.mean(self.waitingtimes)


    def plotQueuelength(self):
        """"shows plot of queuelenght over time"""
        plt.scatter(self.timestamps, self.queuelengths)
        plt.show()

    def saveQueuelengthsToFile(self, fp=False):
        #pickles deque
        if not fp:
            fp = self.fp

        pickle.dump(self.queuelengths)
        print('implement, use self.fp')

    def getProbabilityMatrix(self):
        #returns dict of dicts
        n = len(self.queuelenghts)

