
# Copyright (c) 2015, 2014 Computational Molecular Biology Group, Free University
# Berlin, 14195 Berlin, Germany.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

r"""This module implements the transition matrix covariance function

.. moduleauthor:: B.Trendelkamp-Schroer <benjamin DOT trendelkamp-schroer AT fu-berlin DOT de>

"""
from __future__ import absolute_import
from __future__ import division

import numpy as np
from six.moves import range


def tmatrix_cov(C, row=None):
    r"""Covariance tensor for the non-reversible transition matrix ensemble

    Normally the covariance tensor cov(p_ij, p_kl) would carry four indices
    (i,j,k,l). In the non-reversible case rows are independent so that
    cov(p_ij, p_kl)=0 for i not equal to k. Therefore the function will only 
    return cov(p_ij, p_ik).    

    Parameters
    ----------
    C : (M, M) ndarray
        Count matrix
    row : int (optional)
        If row is given return covariance matrix for specified row only

    Returns
    -------
    cov : (M, M, M) ndarray
        Covariance tensor

    """

    if row is None:
        alpha = C + 1.0  # Dirichlet parameters
        alpha0 = alpha.sum(axis=1)  # Sum of paramters (per row)

        norm = alpha0 ** 2 * (alpha0 + 1.0)

        """Non-normalized covariance tensor"""
        Z = -alpha[:, :, np.newaxis] * alpha[:, np.newaxis, :]

        """Correct-diagonal"""
        ind = np.diag_indices(C.shape[0])
        Z[:, ind[0], ind[1]] += alpha0[:, np.newaxis] * alpha

        """Covariance matrix"""
        cov = Z / norm[:, np.newaxis, np.newaxis]

        return cov

    else:
        alpha = C[row, :] + 1.0
        return dirichlet_covariance(alpha)


def dirichlet_covariance(alpha):
    r"""Covariance matrix for Dirichlet distribution.

    Parameters
    ----------
    alpha : (M, ) ndarray
        Parameters of Dirichlet distribution
    
    Returns
    -------
    cov : (M, M) ndarray
        Covariance matrix
        
    """
    alpha0 = alpha.sum()
    norm = alpha0 ** 2 * (alpha0 + 1.0)

    """Non normalized covariance"""
    Z = -alpha[:, np.newaxis] * alpha[np.newaxis, :]

    """Correct diagonal"""
    ind = np.diag_indices(Z.shape[0])
    Z[ind] += alpha0 * alpha

    """Covariance matrix"""
    cov = Z / norm

    return cov


def error_perturbation_single(C, S, R=None):
    r"""Error-perturbation arising from a given sensitivity

    Parameters
    ----------
    C : (M, M) ndarray
        Count matrix
    S : (M, M) ndarray
        Sensitivity matrix
    R : (M, M) ndarray (optional)
        Sensitivity matrix

    Returns
    -------
    var : float
         Variance (covariance) of observable(s)

    """
    cov = tmatrix_cov(C)  # (M, M, M)
    if R is None:
        R = S
    X = S[:, :, np.newaxis] * cov * R[:, np.newaxis, :]
    return X.sum()


def error_perturbation_var(C, S):
    r"""Error-perturbation arising from a given sensitivity

    Parameters
    ----------
    C : (M, M) ndarray
        Count matrix
    S : (K, M, M) ndarray
        Sensitivity tensor

    """
    K = S.shape[0]
    cov = tmatrix_cov(C)
    for i in range(K):
        R = S[i, :, :]
        X[i] = (R[:, :, np.newaxis] * cov * R[:, np.newaxis, :]).sum()


def error_perturbation_cov(C, S):
    r"""Error-perturbation arising from a given sensitivity

    Parameters
    ----------
    C : (M, M) ndarray
        Count matrix
    S : (K, M, M) ndarray
        Sensitivity tensor

    Returns
    -------
    X : (K, K) ndarray
        Covariance matrix for given sensitivity

    """
    K = S.shape[0]
    X = np.zeros((K, K))
    cov = tmatrix_cov(C)
    for i in range(K):
        for j in range(K):
            Q = S[i, :, :]
            R = S[j, :, :]
            X[i, j] = (Q[:, :, np.newaxis] * cov * R[:, np.newaxis, :]).sum()
    return X


def error_perturbation(C, S):
    r"""Error perturbation for given sensitivity matrix.

    Parameters
    ----------
    C : (M, M) ndarray
        Count matrix
    S : (M, M) ndarray or (K, M, M) ndarray
        Sensitivity matrix (for scalar observable) or sensitivity
        tensor for vector observable
        
    Returns
    -------
    X : float or (K, K) ndarray
        error-perturbation (for scalar observables) or covariance matrix
        (for vector-valued observable)
        
    """
    if len(S.shape) == 2:  # Scalar observable
        return error_perturbation_single(C, S)
    elif len(S.shape) == 3:  # Vector observable
        return error_perturbation_cov(C, S)
    else:
        raise ValueError("Sensitivity matrix S has to be a 2d or 3d array")    