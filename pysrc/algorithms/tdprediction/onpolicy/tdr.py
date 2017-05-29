import numpy as np
from scipy.sparse import csc_matrix as sp
from pysrc.algorithms.tdprediction.tdprediction import TDPrediction
from pysrc.utilities.kanerva_coding import BaseKanervaCoder
from pysrc.utilities.Prototype_MetaGradientDescent import MetaGradientDescent

class TDR(TDPrediction):
    """ TD REPLACING TRACES """

    def __init__(self, config):
        '''Constructor'''
        self.nf = config['nf']
        self.th = np.zeros(self.nf)
        self.z = np.zeros(self.nf)
        try:
            self.alpha = config['alpha'] / config['active_features']
        except KeyError:
            self.alpha = config['alpha']
        
    def initepisode(self):
        self.z = np.zeros(self.nf)
    
    def step(self, params):
        phi=params['phi'];
        R=params['R'];
        phinext=params['phinext']
        g=params['g'];
        l=params['l'];
        gnext=params['gnext']

        delta = R + gnext*np.dot(phinext, self.th) - np.dot(phi, self.th)
        self.z = g*l*self.z*(phi==0.) + (phi!=0.)*phi
        self.th += self.alpha*delta*self.z


class TDR_alpha_bound(TDR):

    def __init__(self, config):
        """    Constructor """
        self.nf = config['nf']
        self.th = np.zeros(self.nf)
        self.z = np.zeros(self.nf)
        self.alpha = config['alpha']

    def step(self, params):
        phi = params['phi']
        r = params['R']
        phinext = params['phinext']
        g = params['g']
        l = params['l']
        gnext = params['gnext']

        delta = r + gnext * np.dot(phinext, self.th) - np.dot(phi, self.th)
        self.z = g * l * self.z * (phi == 0.) + (phi != 0.) * phi
        self.alpha = min(self.alpha, np.abs(np.dot(self.z, (gnext * phinext - phi)))**(-1))
        self.th += self.alpha * delta * self.z


class TDRMSProp(TDR):

    def __init__(self, config):
        super(TDRMSProp, self).__init__(config)
        self.decay = config['decay']
        self.eta = self.alpha
        self.gradient_avg = np.zeros(self.nf)

    def step(self, params):
        phi = params['phi']
        r = params['R']
        phinext = params['phinext']
        g = params['g']
        l = params['l']
        gnext = params['gnext']

        delta = r + gnext*np.dot(phinext, self.th) - np.dot(phi, self.th)
        self.z = g * l * self.z * (phi == 0.) + (phi != 0.) * phi
        self.gradient_avg = self.decay*self.gradient_avg + (1-self.decay)*phi**2  # removed the neg cause of ^2
        self.alpha = self.eta / (np.sqrt(self.gradient_avg) + 10.0 ** (-8))
        self.th += self.alpha * delta * self.z


class TDR_Kanerva(TDPrediction):

    def __init__(self, config):
        self.mu = 0.01
        self.tau = 1 / 10000.

        self.nf = config['nf']
        self.th = np.zeros(self.nf)
        self.v = np.zeros(self.nf)
        self.h = np.zeros(self.nf)
        self.ones = np.ones(self.nf)
        self.z = np.zeros(self.nf)

        try:
          self.initalpha = config['alpha'] / config['active_features']
        except KeyError:
          self.initalpha = config['alpha']
        self.alpha = np.ones(self.nf) * self.initalpha
        self.kanerva = BaseKanervaCoder(
            _startingPrototypes=1024,
            _dimensions=4,
            _numActiveFeatures=config['active_features'])

    def step(self, params):
        phi = params['phi']
        R = params['R']
        phinext = params['phinext']
        g = params['g']
        l = params['l']
        gnext = params['gnext']
        self.kanerva.calculate_f(phi)

        phi = self.kanerva.get_features(phi)
        phinext = self.kanerva.get_features(phinext)

        delta = R + gnext*np.dot(phinext, self.th) - np.dot(phi, self.th)
        self.z = g*l*self.z*(phi==0.) + (phi!=0.)*phi
        self.th += self.alpha*delta*self.z
        self.kanerva.update_prototypes(self.alpha, delta, phi, self.th)

    def estimate(self, phi):
        return np.dot(self.kanerva.get_features(phi), self.th)


class TDR_MGD(TDR):

    def __init__(self, config):
        self.nf = config['nf']
        self.th = np.zeros(self.nf)
        self.v = np.zeros(self.nf)
        self.h = np.zeros(self.nf)
        self.ones = np.ones(self.nf)
        self.z = np.zeros(self.nf)
        try:
          self.initalpha = config['alpha'] / config['nf']
        except KeyError:
          self.initalpha = config['alpha']
        self.alpha = np.ones(self.nf) * self.initalpha
        self.mgd = MetaGradientDescent(_startingPrototypes=config['nf'], _dimensions=4)

    def step(self, params):
        phi = params['phi']
        r = params['R']
        phinext = params['phinext']
        g = params['g']
        l = params['l']
        gnext = params['gnext']

        obs = phi

        phi = self.mgd.get_features(phi)
        phinext = self.mgd.get_features(phinext)

        delta = r + gnext * np.dot(phinext, self.th) - np.dot(phi, self.th)
        self.z = g * l * self.z * (phi==0.) + (phi != 0.) * phi
        self.th += self.alpha*delta*self.z

        self.mgd.update_prototypes(obs, self.alpha, delta, self.th)
 
    def estimate(self, phi):
        phi = self.mgd.get_features(phi)
        return np.dot(phi, self.th)