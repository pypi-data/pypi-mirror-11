
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

r"""This module contains function for the Transition Path Theory (TPT)
analysis of Markov models.

__moduleauthor__ = "Benjamin Trendelkamp-Schroer, Frank Noe"

"""
from __future__ import absolute_import
import numpy as np

from scipy.sparse import diags, coo_matrix, csr_matrix
from six.moves import range


def remove_negative_entries(A):
    r"""Remove all negative entries from sparse matrix.

        Aplus=max(0, A)

    Parameters
    ----------
    A : (M, M) scipy.sparse matrix
        Input matrix

    Returns
    -------
    Aplus : (M, M) scipy.sparse matrix
        Input matrix with negative entries set to zero.

    """
    A = A.tocoo()

    data = A.data
    row = A.row
    col = A.col

    """Positive entries"""
    pos = data > 0.0

    datap = data[pos]
    rowp = row[pos]
    colp = col[pos]

    Aplus = coo_matrix((datap, (rowp, colp)), shape=A.shape)
    return Aplus


# ======================================================================
# Flux matrix operations
# ======================================================================


def flux_matrix(T, pi, qminus, qplus, netflux=True):
    r"""Compute the flux.
    
    Parameters
    ----------
    T : (M, M) scipy.sparse matrix
        Transition matrix
    pi : (M,) ndarray
        Stationary distribution corresponding to T
    qminus : (M,) ndarray
        Backward comittor
    qplus : (M,) ndarray
        Forward committor
    netflux : boolean
        True: net flux matrix will be computed  
        False: gross flux matrix will be computed
    
    Returns
    -------
    flux : (M, M) scipy.sparse matrix
        Matrix of flux values between pairs of states.
    
    """
    D1 = diags((pi * qminus,), (0,))
    D2 = diags((qplus,), (0,))

    flux = D1.dot(T.dot(D2))

    """Remove self-fluxes"""
    flux = flux - diags(flux.diagonal(), 0)

    """Return net or gross flux"""
    if netflux:
        return to_netflux(flux)
    else:
        return flux


def to_netflux(flux):
    r"""Compute the netflux.
    
    f_ij^{+}=max{0, f_ij-f_ji}
    for all pairs i,j
    
    Parameters
    ----------
    flux : (M, M) scipy.sparse matrix
        Matrix of flux values between pairs of states.
    
    Returns
    -------
    netflux : (M, M) scipy.sparse matrix
        Matrix of netflux values between pairs of states.
    
    """
    netflux = flux - flux.T

    """Set negative entries to zero"""
    netflux = remove_negative_entries(netflux)
    return netflux


def coarsegrain(F, sets):
    r"""Coarse-grains the flux to the given sets
    
    $fc_{i,j} = \sum_{i \in I,j \in J} f_{i,j}$
    Note that if you coarse-grain a net flux, it does not necessarily have a net
    flux property anymore. If want to make sure you get a netflux, 
    use to_netflux(coarsegrain(F,sets)).
    
    Parameters
    ----------
    F : (n, n) ndarray
        Matrix of flux values between pairs of states.
    sets : list of array-like of ints
        The sets of states onto which the flux is coarse-grained.
    
    """
    nnew = len(sets)
    Fin = F.tocsr()
    Fc = csr_matrix((nnew, nnew))
    for i in range(0, nnew - 1):
        for j in range(i, nnew):
            I = list(sets[i])
            J = list(sets[j])
            Fc[i, j] = (Fin[I, :][:, J]).sum()
            Fc[j, i] = (Fin[J, :][:, I]).sum()
    return Fc


# ======================================================================
# Total flux, rate and mfpt for the A->B reaction
# ======================================================================


def total_flux(flux, A):
    r"""Compute the total flux between reactant and product.
    
    Parameters
    ----------
    flux : (M, M) scipy.sparse matrix
        Matrix of flux values between pairs of states.
    A : array_like
        List of integer state labels for set A (reactant)
    
    Returns
    -------
    F : float
        The total flux between reactant and product
    
    """
    X = set(np.arange(flux.shape[0]))  # total state space
    A = set(A)
    notA = X.difference(A)

    """Extract rows corresponding to A"""
    W = flux.tocsr()
    W = W[list(A), :]
    """Extract columns corresonding to X\A"""
    W = W.tocsc()
    W = W[:, list(notA)]

    F = W.sum()
    return F