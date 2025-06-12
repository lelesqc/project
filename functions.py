import numpy as np
from scipy.special import ellipk, ellipe
from sage.functions.jacobi import inverse_jacobi, jacobi
from scipy.optimize import brentq
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR))

import params as par

# ------------------ functions -------------------------

def H0_for_action_angle(q, p):
    Q = (q + np.pi) / par.lambd
    P = par.lambd * p
    return 0.5 * P**2 - par.A**2 * np.cos(par.lambd * Q)

def compute_action_angle(kappa_squared, P):
    action = 8 * par.A / np.pi * (ellipe(kappa_squared) - (1 - kappa_squared) * ellipk(kappa_squared))
    K_of_kappa = (ellipe(kappa_squared) - (np.pi * action)/(8 * par.A)) / (1 - kappa_squared)
    Omega = np.pi / 2 * (par.A / K_of_kappa)
    x = P / (2 * np.sqrt(kappa_squared) * par.A)
    
    u = inverse_jacobi('cn', float(x), float(kappa_squared))
    theta = (Omega / par.A) * u
    return action, theta
    
def dV_dq(q):  
    return par.A**2 * np.sin(q)

def Delta_q(p, t, dt, step):
    return par.lambd**2 * p * dt + par.a_lambda(step) * par.omega_lambda(step) * np.sin(par.omega_lambda(step) * t + par.phi_0) * dt

def compute_I_from_h0(h0, A):
    kappa_squared = 0.5 * (1 + h0 / (A**2))
    if kappa_squared < 0 or kappa_squared > 1:
        return np.inf
    K = ellipk(kappa_squared)
    E = ellipe(kappa_squared)
    I = (8 * A / np.pi) * (E - (1 - kappa_squared) * K)
    return I

def compute_action_angle_inverse(X, Y):
    action = (X**2 + Y**2) / (2)
    theta = np.arctan2(-Y, X)
    return action, theta

def compute_Q_P(theta, Omega, kappa_squared):
    Q = 2 / par.lambd * np.arccos(jacobi('dn', float(par.A * theta / Omega), float(kappa_squared))) * np.sign(np.sin(theta))
    P = 2 * np.sqrt(kappa_squared) * par.A * jacobi('cn', float(par.A * theta / Omega), float(kappa_squared))
    return Q, P

def compute_phi_delta(Q, P):
    delta = P / par.lambd
    phi = par.lambd * Q - np.pi
    return phi, delta

def find_h0_numerical(I_target):
    def G_objective(h0_val):
        m = 0.5 * (1 + h0_val / par.A**2)
        epsilon = 1e-12
        m = np.clip(m, epsilon, 1 - epsilon)
        return (8 * par.A / np.pi) * (ellipe(m) - (1 - m) * ellipk(m)) - I_target

    epsilon_h = 1e-9 * par.A**2
    return brentq(G_objective, -par.A**2 + epsilon_h, par.A**2 - epsilon_h)

def update_omega_m(update_freq):
    if update_freq:
        par.omega_m += .5 * par.Delta_omega / par.n_steps
