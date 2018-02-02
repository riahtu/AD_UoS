#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inludes all supporting functions for gsp disaggregation
Created on Fri Feb  2 12:09:27 2018

@author: haroonr
"""
def gspclustering(event,delta_p,sigma):
  
  winL = 1000
  Smstar = np.zeros((len(event),1))
  #for k in range(0,len(event),winL):
  for k in range(0,int(np.floor(len(event)/winL))):
    r = []
    print('k val is {}'.format(k))
    event_1 =  event[k*winL:((k+1)*winL)]
    r.append(delta_p[event[0]])
    [r.append(delta_p[i]) for i in event_1]
    Sm = np.zeros((winL+1,1))
    Sm[0] = 1;
    Am = np.zeros((winL,winL))
    for i in range(winL):
      for j in range(winL):
         #print(i,j)
         #print('\n')
         Am[i,j] = np.exp(-((r[i]-r[j])/sigma)**2);
         #Gaussian kernel weighting function
    Dm = np.zeros((winL,winL));
    for i in range(winL):
      Dm[i,i] = np.sum(Am[:,i]);
    Lm = Dm - Am;
    Smstar[k*winL:((k+1)*winL)] = np.matmul(np.linalg.pinv(Lm[0:winL,0:winL]), ((-Sm[0].T) * Lm[0,0:winL]).reshape(-1,1));
  # for remaining elements of the event list
  if (len(event)%winL > 1):
    r = []
    #print('k val is {}'.format(k))
    event_1 =  event[int(np.floor(len(event)/winL))*winL:]
    newlen = len(event_1)
    r.append(delta_p[event[0]])
    [r.append(delta_p[i]) for i in event_1]
    Sm = np.zeros((newlen,1))
    Sm[0] = 1;
    Am = np.zeros((newlen,newlen))
    for i in range(newlen):
      for j in range(newlen):
         #print(i,j)
         #print('\n')
         Am[i,j] = np.exp(-((r[i]-r[j])/sigma)**2);
         #Gaussian kernel weighting function
    Dm = np.zeros((newlen,newlen));
    for i in range(newlen):
      Dm[i,i] = np.sum(Am[:,i]);
    Lm = Dm - Am;
    Smstar_temp = np.matmul(np.linalg.pinv(Lm[0:newlen,0:newlen]), ((-Sm[0].T) * Lm[0,0:newlen]).reshape(-1,1));
    Smstar[(int(np.floor(len(event)/winL))*winL):len(event)] = Smstar_temp
  cluster = [event[i] for i in range(len(Smstar)) if (Smstar[i] > 0.98)]
  return cluster
