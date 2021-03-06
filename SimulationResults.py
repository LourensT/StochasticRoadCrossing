import numpy as np
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import itertools
from datetime import datetime
import csv
import pickle

class SimulationResults:
    """used to store relevant datapoints during a simulation """
    def __init__(self, s, m, h, T):
        
        dt = datetime.now().strftime("%H-%M-%S")
        self.fp = "{}_s_{}_m_{}h_{}timebound_{}.pickle".format(dt, s, m, h, T)

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

    def getFinalQueueLength(self):
        return self.queuelengths.pop()

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

    def pickleQueueLengths(self, fp=False):
        """pickles deque"""
        if not fp:
            fp = self.fp

        pickle.dump(self.queuelengths, open(fp, 'wb'))
        print('dumped sucessfully')

    def getProbabilityMatrix(self, fp=False):
        """calculates and return probability matrix"""
        #find  deque of queuelengths
        ql = self.queuelengths
        n = len(ql) - 1

        #get frequency matrix
        matr = defaultdict(dict)
        prev_state = ql.popleft()
        while ql:
            state = ql.popleft()
            if state in matr[prev_state]:
                matr[prev_state][state] += 1   
            else:
                matr[prev_state][state] = 1
            prev_state = state   

        #normalize
        samplesizes = []
        stoch_matr = np.zeros((10, 10))
        for k, v in matr.items():
            if k < 10:
                freq = sum(v.values())
                samplesizes.append(freq)
                for i, j  in v.items():
                    if i < 10:
                        stoch_matr[k, i] = round(j / freq, 5)

        ci_matrix = []
        for i in range(len(stoch_matr)):
            ci_row = []
            n = samplesizes[i]
            for j in stoch_matr[i]:
                halfwidth = 1.96 * (((j*(1-j))/n)**(1/2))
                ci_row.append([j-halfwidth, j+halfwidth])
            ci_matrix.append(ci_row)

        if fp: 
            with open(fp, 'w', encoding='utf-8') as f:
                f.write('samplesizes')
                f.write('\n')
                f.write(str(samplesizes))
                f.write('\n')
                f.write('estimates')
                f.write('\n')
                f.write(str(np.array(stoch_matr)))
                f.write('\n')
                f.write('confidence intervals')
                f.write('\n')
                f.write(str(np.array(ci_matrix)))

        print(samplesizes)
        return np.array(stoch_matr)



        

        



