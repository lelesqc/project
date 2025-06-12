import numpy as np
import functions as fn
import utils
import params as par
from tqdm.auto import tqdm

def run_action_angle():
    action_list = []
    theta_list = []
    sign_list = []
    
    nu_m = par.omega_m / par.omega_s
    filepath = utils.get_output_filepath("integrator", par.a, nu_m)
    data = np.load(filepath)
    q, p = data['q_arr'], data['p_arr']  

    for i in tqdm(range(len(q))):
        h_0 = fn.H0_for_action_angle(q[i], p[i])
        kappa_squared = 0.5 * (1 + h_0 / (par.A**2))

        if 0 < kappa_squared < 1:
            Q = (q[i] + np.pi) / par.lambd
            P = par.lambd * p[i]

            action, theta = fn.compute_action_angle(kappa_squared, P)
            action_list.append(action)
            theta_list.append(theta)
            sign_list.append(np.sign(q[i]-np.pi))

    action_list = np.array(action_list)
    theta_list = np.array(theta_list)

    x = np.sqrt(2 * np.array(action_list)) * np.cos(theta_list)
    y = - np.sqrt(2 * np.array(action_list)) * np.sin(theta_list) * np.array(sign_list)

    # --------------- Save results ----------------

    nu_m = par.omega_m / par.omega_s
    filepath = utils.get_output_filepath("cartesian", par.a, nu_m)
    np.savez(filepath, action=action_list, theta=theta_list, X=x, Y=y)
    print(f"Data saved in: {filepath}")

if __name__ == "__main__":
    run_action_angle()
    print("Action-angle coordinates computed and saved successfully.")