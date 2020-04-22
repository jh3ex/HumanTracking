# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:38:30 2020

Bayesian Robotics course project:
    Probabilistic sensor model

@author: jingh
"""

import numpy as np
import pandas as pd
from scipy.stats import norm, multivariate_normal
import copy


class ProbSensorModel:
    def __init__(self, ov_mu, ov_sigma):
        self.ov_mu = ov_mu
        self.ov_sigma = ov_sigma


    def correction(self, ox, oy, xt):
        """
        Calculate likelihood given an observation
        Arguments:
            ox:  observed x
            oy:  observed y
            xt:  particles
        Return:
            xt with updated weights
        """

        for i in range(xt.count()[0]):



            mean = np.array([xt['x'].loc[i], xt['y'].loc[i]]) + self.ov_mu

            # Likelihood
            p_zx = multivariate_normal.pdf(np.array([ox, oy]), mean, self.ov_sigma)

            # Update weight
            xt['weight'].loc[i] = p_zx

        return xt
