import numpy as np
import sys
import yaml

# ------------ machine ----------------

h = 328
eta = 1.26e-3
nu_s = 0.0075
omega_rev = 9_571_303.971
omega_s = 77625.3184
V = 1.5e6
E_s = 1.5e9

# -------------- model -----------------

damp_rate = 38.1
beta = 1.0
D = 1.82e-3
N = 100    # fixed
N_turn = 20000
phi_0 = 0.0
e = 1
a = 0.1
lambd = np.sqrt(h * eta * omega_rev)
A = omega_s / lambd

# -------------- YAML --------------------

if len(sys.argv) > 1:
    config_path = sys.argv[1]
else:
    config_path = "params.yaml"  # default

with open(config_path) as f:
    config = yaml.safe_load(f)

a_max = config["a"]
nu_m_i = config["nu_m_i"]
nu_m_f = config["nu_m_f"]

omega_m_i = nu_m_i * omega_s
omega_m_f = nu_m_f * omega_s

# ------------- variables -----------------

T_s = 2 * np.pi / omega_s
dt = T_s / N
T_mod = 2 * np.pi / omega_m_f
steps = int(round(T_mod / dt))
n_steps = steps * N_turn

t = 0.0

# ------------- lambda functions ------------

a_lambda = lambda step: a_max * step / (0.1 * n_steps) if step < 0.1 * n_steps else a_max
nu_lambda = lambda step: nu_m_f if step < 0.1 * n_steps else nu_m_f - (nu_m_f - nu_m_i) * ((step - 0.1 * n_steps) / (n_steps - 0.1 * n_steps))
