# -*- coding: utf-8 -*-

#
# This file is part of UQToolbox.
#
# UQToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# UQToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with UQToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

import sys
import os
import warnings
import logging
import marshal, types
import time
import datetime
import numpy as np
from numpy import linalg as la
from numpy import random
from scipy import stats
from sobol_lib import i4_sobol_generate
from UQToolbox import object_store, Driver
try:
    import mpi_map
    MPI_SUPPORT = True
except ImportError:
    MPI_SUPPORT = False

class MultiDimDistribution():
    """ Tensor construction of a multidimensional distribution
    
    :param list dists: list of distributions along each dimension.
    """

    dists = []
    
    def __init__(self,dists):
        self.dists = dists;
    
    def rvs(self,size):
        """ Samples ``size`` realizations from the multidimensional distribution. Equivalent to Monte Carlo sampling.
        
        :param int size: number of samples
        :returns: list of samples
        """
        samples = np.zeros( (size, len(self.dists)) )
        for i in range(len(self.dists)):
            samples[:,i] = self.dists[i].rvs(size)
        return list(samples)
    
    def lhc(self,size):
        """ Samples ``size`` realizations from the multidimensional distribution using the Latin Hyper Cube method.
        
        :param int size: number of samples
        :returns: list of samples
        """
        d = len(self.dists)
        
        XX = np.zeros((size,d))
        for i in range(0,size):
            XX[i,:] = stats.uniform(loc=(i*1./size),scale=1./size).rvs(size=d)

        P = np.zeros((size,d),dtype=np.int)
        for i in range(0,d):
            P[:,i] = np.arange(0,size)
            random.shuffle(P[:,i])

        for i in range(0,d):
            XX[:,i] = XX[P[:,i],i]

        ''' Convert from uniform to self.dists '''
        udist = stats.uniform(0.,1.);
        if self.dists != None and len(self.dists) == d:
            for i in range(d):
                XX[:,i] = self.dists[i].ppf(udist.cdf(XX[:,i]))

        return list(XX)
    
    def sobol(self,size,skip=None):
        """ Samples ``size`` realizations from the multidimensional distribution using the Sobol sequence for Quasi Monte Carlo method.
        
        :param int size: number of samples
        :returns: list of samples
        """
        if skip == None:
            dim = len(self.dists)
            skip = int( np.random.uniform(2**np.ceil(np.log2(dim+1)), 2**(np.ceil(np.log2(dim+1))+1)) )
        unifSamples = i4_sobol_generate(len(self.dists),size,skip); 
        samples = np.zeros(unifSamples.T.shape);
        for i in range(0,len(self.dists)):
            samples[:,i] = self.dists[i].ppf(unifSamples[i,:])
        
        return list(samples)
    
class RandomExperiments(Driver):
    """ This class is devoted to the sampling from a multi dimensional distribution and the evaluation of a function `f` on it.
    
    :param function f: the function representing the experiment
    :param object params: parameters to be passed to the function ``f`` (pickable)
    :param list dists: list of distributions, instance of ``scipy.stats``
    :param bool marshal_f: whether to marshal the function ``f`` or not.
    :param str store_file: file path where to store the computed values
    """

    logger = logging.getLogger(__name__)
    logger.propagate = False
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s:%(name)s: %(message)s",
                                  "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
        
    def __init__(self, f, params, dists, marshal_f=True, store_file=""):

        super(RandomExperiments,self).__init__(f, params, marshal_f, store_file)
        
        self.dists = None
        self.mdist = None
        
        self.set_dists(dists)

    def __getstate__(self):
        return super(RandomExperiments,self).__getstate__()

    def __setstate__(self,state,f = None, dists=None):
        super(RandomExperiments,self).__setstate__( state, f )
        if dists != None:
            self.set_dists( dists )
            
    def set_dists(self, dists):
        self.dists = dists
        self.mdist = MultiDimDistribution(dists)
    
    def get_mdist(self):
        return self.mdist
    
    def sample(self, size, method='mc', append=True):
        """ Sample from the multidimensional distribution defined by the ``dists``.
        
        :param int size: the size of the sample set
        :param str method: the sampling method to be used. Options are: 'mc' for Monte Carlo, 'lhc' for Latin Hyper Cube, 'sobol' for Quasi Monte Carlo with Sobol sequence.
        :param bool append: if True, the new samples are appended to the old samples. Using run() will apply the experiments on only the new samples. If False, the old samples and old results are discarded. This is possible only for methods 'mc' and 'lhc'.

        :note: If the Experiments object has been reloaded using pickle, the ``dists`` parameters should be reset using ``set_dists``.
        """
        if self.mdist == None:
            raise RuntimeError("UQToolbox.RandomSampling.Experiments.sample: No distribution set. Use UQToolbox.RandomSampling.Experiments.set_dists to set the distribution.")
        
        if append == False or method == 'sobol':
            self.reset()
        
        if method == 'mc':
            self.new_samples.extend( self.mdist.rvs(size) )
        elif method == 'lhc':
            self.new_samples.extend( self.mdist.lhc(size) )
        elif method == 'sobol':
            self.new_samples.extend( self.mdist.sobol(size) )
        else:
            raise RuntimeError("UQToolbox.RandomSampling.Experiments.sample: The proposed method is not available.")

Experiments = RandomExperiments

def run_experiments(f,samples,params,paramUpdate,action):
    """
    Compute the Experiments f on the samples.
    The implementation uses MPI for parallel computations.

    :param function f: experiment function handle. Signature: f( params )
    :param samples: nd-array with the set of samples grouped by the first dimension
    :param params: set of parameters to be passed to the experiment
    :param function action: post processing action

    :returns: Array of computed values, ordered by the first dimension of the array.

    ..deprecated:: 0.1.5
    """
    warnings.warn("UQToolbox.RandomSampling.run_experiments: Deprecated function", DeprecationWarning)
    
    def iterF(f,samples,params,paramUpdate,action):
        sols = []
        for i in xrange(0,samples.shape[0]):
            params = paramUpdate(params,samples[i])
            sol = f(params)
            print "Proc %d run %d/%d" % (myrank,i+1,len(samples))
            sols = action(sols,sol)
        return sols
    
    comm = MPI.COMM_WORLD
    nprocs = comm.Get_size()
    myrank = comm.Get_rank()
    
    if myrank == 0:
        # Split the input array
        splittedSamples = np.array_split(samples,nprocs)
        startTime = time.clock()
    else:
        splittedSamples = None
    
    samplesPart = comm.scatter(splittedSamples,root=0)
    
    splittedSolutions = iterF(f,samplesPart,params,paramUpdate,action)
    
    solutionsList = comm.gather(splittedSolutions)
    
    if myrank == 0:
        # Reassemble post processing data
        # To be fixed for MPI!!!!!! Use the proper action..
        solutions = [inner for outer in solutionsList for inner in outer]

        stopTime = time.clock()
        print "Elapsed Time: %f s" % (stopTime-startTime)
        
        return solutions

def MonteCarlo(dists,N,experiment,params,paramUpdate,postProc):
    """
    Run Monte Carlo Simulations
    
    ..deprecated:: 0.1.5
    """
    warnings.warn("UQToolbox.RandomSampling.MonteCarlo: Deprecated function", DeprecationWarning)

    mdd = MultiDimDistribuion(dists);
    samples = mdd.rvs(N)
    return (samples,run_experiments(experiment, samples, params, paramUpdate, postProc))

def QuasiMonteCarlo(dists,N,experiment,params,paramUpdate,postProc,skip=None):
    """
    Run Quasi Monte Carlo Simulations

    ..deprecated:: 0.1.5
    """
    warnings.warn("UQToolbox.RandomSampling.QuasiMonteCarlo: Deprecated function", DeprecationWarning)

    # Generate uniformly distributed samples using Sobol sequence
    if skip == None:
        dim = len(dists)
        skip = int( np.random.uniform(2**np.ceil(np.log2(dim+1)), 2**(np.ceil(np.log2(dim+1))+1)) )
    unifSamples = i4_sobol_generate(len(dists),N,skip); 
    samples = np.zeros(unifSamples.T.shape);
    for i in range(0,len(dists)):
        samples[:,i] = dists[i].ppf(unifSamples[i,:])
    return (samples,run_experiments(experiment, samples, params, paramUpdate, postProc), skip)

def lhc(N,d,dists=None):
    """
    Latin Hyper Cube

    ..deprecated:: 0.1.5
    """
    warnings.warn("UQToolbox.RandomSampling.lhc: Deprecated function", DeprecationWarning)

    XX = np.zeros((N,d))
    for i in range(0,N):
        XX[i,:] = stats.uniform(loc=(i*1./N),scale=1./N).rvs(size=d)
    
    P = np.zeros((N,d),dtype=np.int)
    for i in range(0,d):
        P[:,i] = np.arange(0,N)
        random.shuffle(P[:,i])
    
    for i in range(0,d):
        XX[:,i] = XX[P[:,i],i]
    
    ''' Convert from uniform to dists '''
    udist = stats.uniform(0.,1.);
    if dists != None and len(dists) == d:
        for i in range(d):
            XX[:,i] = dists[i].ppf(udist.cdf(XX[:,i]))
    
    return XX

def LatinHyperCube(dists,N,experiment,params,paramUpdate,postProc):
    """
    Run Latin Hyper Cube Simulations
    
    ..deprecated:: 0.1.5
    """
    warnings.warn("UQToolbox.RandomSampling.LatinHyperCube: Deprecated function", DeprecationWarning)

    samples = lhc(N,len(dists),dists)
    return (samples,run_experiments(experiment, samples, params, paramUpdate, postProc))
