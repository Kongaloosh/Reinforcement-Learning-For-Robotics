"""specifies the configuration for the algorithms"""
import numpy as np
import cPickle as pickle

alphas = [0.05, 0.1, 0.2, 0.3, 0.6, 1.0, 1.5, 2.0]
# alphas = [0.1]
# lambdas = [0.99]
num_features = [100, 500, 1000, 2000, 5000, 10000]
lambdas = [0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.98, 0.99, 0.995, 0.998, 0.999, 1]

configs =[{'alpha': alpha, 'lmbda': lm, 'nf':num_feature} for alpha in alphas for lm in lambdas for num_feature in num_features]

print len(configs)
f = open('configalg.pkl', 'wb')
pickle.dump(configs, f)