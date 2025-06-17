import numpy as np
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
N_turn = 10000
phi_0 = 0.0
e = 1
lambd = np.sqrt(h * eta * omega_rev)
A = omega_s / lambd

# -------------- YAML --------------------

config_path = "params.yaml"

with open(config_path) as f:
    config = yaml.safe_load(f)

epsilon_i = config["epsilon_i"]
epsilon_f = config["epsilon_f"]
nu_m_i = config["nu_m_i"]
nu_m_f = config["nu_m_f"]

omega_m_i = nu_m_i * omega_s
omega_m_f = nu_m_f * omega_s

Delta_eps = epsilon_f - epsilon_i
Delta_omega = (nu_m_f - nu_m_i) * omega_s

# ------------- variables -----------------

T_s = 2 * np.pi / omega_s
dt = T_s / N
T_mod = 2 * np.pi / omega_m_f
steps = int(round(T_mod / dt))
n_steps = steps * N_turn
print(f"Number of steps: {dt}")

t = 0.0

# ------------- lambda functions -----------

percent = 0.1

T_tot = n_steps * dt
T_percent = percent * T_tot

#epsilon_function = lambda t: -2.5*10e-3 * (t-T_percent)**2/(T_tot-T_percent)**2 + 0.02 * (t-T_percent)/(T_tot-T_percent) + epsilon_i
epsilon_function = lambda t: (omega_m_i + Delta_omega * (t - T_percent) / (T_tot - T_percent)) * (0.025 + 0.025 * (t - T_percent) / (T_tot - T_percent))
epsilon = lambda t: epsilon_i * (t / T_percent) if t < T_percent else epsilon_function(t)

omega_lambda = lambda t: omega_m_i if t < T_percent else omega_m_i + (Delta_omega) * ((t - T_percent) / (T_tot - T_percent))
a_lambda = lambda t: epsilon(t) / omega_lambda(t)