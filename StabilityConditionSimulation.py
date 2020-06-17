from scipy import stats
from collections import deque
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

from Simulation import Simulation, Car

parameters = {  0.1 : (0.091, 0.182), 
                0.2 : (0.168, 0.336),
                0.3 : (0.235, 0.470),
                0.4 : (0.294, 0.588),
                0.5 : (0.347, 0.693),
                0.6 : (0.394, 0.788),
                0.7 : (0.438, 0.875),
                0.8 : (0.478, 0.956),
                0.9 : (0.515, 1.030),
                1.1 : (0.549, 1.099)}

results = {}
nrRuns = 500
for k, v in parameters.items():
    print(k)
    
    sim = Simulation(v[0],v[1], 1)
    lengths = np.zeros(nrRuns)
    for i in range(nrRuns):
        res = sim.simulate(1000, immediate_departure=False)
        lengths[i] = res.getFinalQueueLength()
    results[k] = (np.mean(lengths), 2*1.96* (np.std(lengths)/(nrRuns)**(1/2)))


print(results)
plt.errorbar(results.keys(), [v[0] for v in results.values()], yerr=[v[1] for v in results.values()], ecolor='black', capsize=2)
plt.scatter(results.keys(), [v[0] for v in results.values()])
plt.xlabel("Load")
plt.ylabel("Mean Queulength after 1000 time-units")
plt.title("Impact of Load on Queuelength (with 95-CI), case 1")
plt.grid(True)
plt.show()        
