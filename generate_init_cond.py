import numpy as np
import functions as fn
import params as par
import utils
import random
import argparse
from scipy.special import ellipk

def generate_init(radius, n_particles, seed):

    random.seed(seed)

    X_list = []
    Y_list = []

    while len(X_list) < n_particles:
        X = random.uniform(-radius, radius)
        Y = random.uniform(-radius, radius)

        if X**2 + Y**2 <= radius*2:
            X_list.append(X)
            Y_list.append(Y)

    X_list = np.array(X_list)
    Y_list = np.array(Y_list)

    action, theta = fn.compute_action_angle_inverse(X_list, Y_list)

    kappa_squared_list = []
    Omega_list = []

    for act in action:
        h_0 = fn.find_h0_numerical(act)
        kappa_squared = 0.5 * (1 + h_0 / (par.A**2))
        kappa_squared_list.append(kappa_squared)
        Omega_list.append(np.pi / 2 * (par.A / ellipk(kappa_squared)))
        
    Q_list = []
    P_list = []

    for angle, freq, k2 in zip(theta, Omega_list, kappa_squared_list):
        Q, P = fn.compute_Q_P(angle, freq, k2)
        Q_list.append(Q)
        P_list.append(P)

    Q = np.array(Q_list)
    P = np.array(P_list) 

    phi, delta = fn.compute_phi_delta(Q, P)
    phi = np.mod(phi, 2 * np.pi) 
    q_init = np.array(phi)
    p_init = np.array(delta)

    # --------------- Save results ----------------

    nu_m = par.omega_m / par.omega_s
    base_filepath = utils.get_output_filepath("init_cond", par.a, nu_m)
    filepath_with_seed = f"{base_filepath}_seed_{seed}.npz"
    
    np.savez(filepath_with_seed, q0=q_init, p0=p_init)   
    print(f"Data saved in: {filepath_with_seed}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate initial conditions for simulation.")
    parser.add_argument("--radius", type=float, required=True, help="Radius of the initial circle.")
    parser.add_argument("--n_particles", type=int, required=True, help="Number of particles to generate.")
    parser.add_argument("--seed", type=int, required=True, help="Random seed for reproducibility.")
    
    args = parser.parse_args()
    
    generate_init(args.radius, args.n_particles, args.seed)
    
    print("Initial conditions generated and saved successfully.")