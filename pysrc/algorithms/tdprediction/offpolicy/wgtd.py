'''
Created on Jan 2015

@author: A. Rupam Mahmood
'''

import numpy as np
import pylab as pl
from pysrc.algorithms.tdprediction.tdprediction import TDPrediction

class WGTD(TDPrediction):
  
  def __init__(self, config):
    
    self.nf = config['nf']
    self.th = np.zeros(self.nf)
    self.z = np.zeros(self.nf)
    self.w = np.zeros(self.nf)
    self.beta = config['beta']
    self.eta    = config['eta']
    self.initd  = config['initd']
    self.d      = np.ones(self.nf)*self.initd
    self.v      = np.zeros(self.nf)
    
  def initepisode(self):
    self.z = np.zeros(self.nf)
    
  def step(self, params):
    phi=params['phi']; R=params['R']; phinext=params['phinext']
    g=params['g']; l=params['l']; gnext=params['gnext']
    rho=params['rho']; lnext=params['lnext']
    
    self.d        = self.d - self.eta*phi*phi*self.d \
            + rho*phi*phi \
            + (rho-1)*g*l*(self.v - self.eta*phi*phi*self.v)
    self.dtemp    = np.copy(self.d)
    self.dtemp[self.dtemp==0.0] = 1
    alpha         = 1/self.dtemp
    self.v        = rho*g*l*(self.v-self.eta*phi*phi*self.v) \
            + rho*phi*phi

    delta = R + gnext*np.dot(phinext,self.th) - np.dot(phi, self.th)
    self.z = rho*(g*l*self.z + phi)
    self.th += delta*alpha*self.z \
      - gnext*(1-lnext)*np.dot(self.z, self.w)*alpha*phinext
    self.w += self.beta*(delta*self.z - np.dot(phi, self.w)*phi)


