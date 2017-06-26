import pickle
import random
import numpy as np
from numpy.random import randn
from numpy.linalg import norm
from sklearn.utils.linear_assignment_ import _hungarian
from filterpy.monte_carlo import systematic_resample
from utils.filter_utils import (create_uniform_particles, create_gaussian_particles,
                                predict, update, estimate, neff, resample_from_index)

import matplotlib.pyplot as plt

from utils import custom_plots


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return ang1 - ang2 # angle in radians


# LOAD THE SYNTHETIC AND TRUTH SEQUENCES
locs1 = pickle.load(open('./input/target_locs_1.pkl', 'rb'), encoding='latin1')
locs2 = pickle.load(open('./input/target_locs_2.pkl', 'rb'), encoding='latin1')
locs3 = pickle.load(open('./input/target_locs_3.pkl', 'rb'), encoding='latin1')
rows, cols = (250,250)


# PARTICLE FILTER SETTINGS
sensor_std_err=0.1
do_plot=True
plot_particles=True
initial_x=None
N = 5000
landmarks = np.array([[1,1], [1,cols-1], [rows-1,1], [rows-1,cols-1]])
NL = len(landmarks)
n_possible_targets = 6
particles_list = []
weights_list = []

pcolors = ['lightblue', 'limegreen', 'gold']


# ITERATE THROUGH THE INPUT FRAMES, DETECTING & P.F. TRACKING
for ifn in range(139):
    print('frame:', ifn)
    frame = np.zeros([rows, cols])
    if ifn not in [50,70, 72, 76]:
        frame[(locs1[ifn][0], locs1[ifn][1])] = 1.0
        frame[(locs2[ifn][0], locs2[ifn][1])] = 1.0
        frame[(locs3[ifn][0], locs3[ifn][1])] = 1.0
    else:
        frame[(locs2[ifn][0], locs1[ifn][1])] = 1.0
        frame[(locs1[ifn][0], locs2[ifn][1])] = 1.0
        frame[(locs3[ifn][0], locs3[ifn][1])] = 1.0        

    dets = np.array([locs1[ifn], locs2[ifn], locs3[ifn]])
    
    # create particles and weights
    for _ in range(len(dets)):
        if initial_x is not None:
            particles = create_gaussian_particles(mean=initial_x, std=(5, 5, np.pi/4), N=N)
        else:
            particles = create_uniform_particles((0,rows), (0,cols), (0, 6.28), N)
        particles_list.append(particles)
        weights = np.zeros(N)
        weights_list.append(weights)
        
    if ifn == 0:
        
        dets_prev = dets        
    
    else:
    
        # determine initial location and heading from dets and dets_prev
        if dets.size > 0:
            # create cost array from detections
            cost = []
            for a in dets:
                dist = [np.linalg.norm(a - b) for b in dets_prev]
                cost.append(dist)
    
            # associate detections
            result = _hungarian(np.array(cost)) 
    
            for ii in range(len(result)):
                cidx, pidx = result[ii]
                robot_pos = dets[cidx][::-1] # expects (x,y) instead of (y,x)
                robot_pos_prev = dets_prev[pidx][::-1]
                #print('Position:', robot_pos, 'Position_prev:', robot_pos_prev)
                heading = angle_between(robot_pos_prev, robot_pos)
                speed = np.linalg.norm(robot_pos - robot_pos_prev)
                particles = particles_list[pidx]
                weights = weights_list[pidx]                  
        
                # distance from robot to each landmark
                zs = (norm(landmarks - robot_pos, axis=1) +
                      (randn(NL) * sensor_std_err))
        
                # move
                predict(particles, u=(speed, heading), std=(0.5, 0.4))
        
                # incorporate measurements
                update(particles, weights, z=zs, R=sensor_std_err,
                       landmarks=landmarks)
                    
                # resample if too few effective particles
                if neff(weights) < N/2:
                    indexes = systematic_resample(weights)
                    resample_from_index(particles, weights, indexes)
        
                mu, var = estimate(particles, weights)               
        
                if plot_particles:
                   plt.scatter(particles[:, 0], particles[:, 1],
                               color='r', marker=',', s=1, alpha=0.05)
                plt1 = plt.scatter(robot_pos[0], robot_pos[1], marker='+',
                                 color='b', s=80, lw=1)
                plt2 = plt.scatter(mu[0], mu[1], marker=',', s=6, color=pcolors[pidx])

    #accept = custom_plots.show_img_return_input(frame, str(ifn), cm='gray', ask=False)
    custom_plots.write_img(frame, str(ifn), './output') 
    dets_prev = dets
    
# plt.legend([plt1, plt2], ['Actual', 'PF'], loc=1, numpoints=1)
# print('final position error, variance:\n\t', mu, var)
# plt.show()
