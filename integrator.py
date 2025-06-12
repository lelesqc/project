import numpy as np
import functions as fn
import params as par
import utils
from tqdm.auto import tqdm

def run_integrator():
    nu_m = par.omega_m / par.omega_s
    filepath = utils.get_output_filepath("init_cond", par.a, nu_m)
    data = np.load(filepath)
    q_init, p_init = data['q0'], data['p0']

    q = q_init.copy()
    p = p_init.copy()

    q_sec, p_sec, t_sec, step_sec = [], [], [], []

    for step in tqdm(range(par.n_steps)):
        q += fn.Delta_q(p, par.t, par.dt/2, par.omega_m)
        q = np.mod(q, 2 * np.pi)
        
        t_mid = par.t + par.dt/2

        p += par.dt * fn.dV_dq(q)

        q += fn.Delta_q(p, t_mid, par.dt/2, par.omega_m)
        q = np.mod(q, 2 * np.pi)

        par.t += par.dt
        
        if np.cos(par.omega_m * par.t) > 1.-1e-5:
            q_sec.append(q.copy())
            p_sec.append(p.copy())
            t_sec.append(par.t)
            step_sec.append(step)
    
    q_sec = np.array(q_sec)
    p_sec = np.array(p_sec)
    t_sec = np.array(t_sec)
    step_sec = np.array(step_sec)

    # --------------- Save results -----------------

    nu_m = par.omega_m / par.omega_s
    filepath = utils.get_output_filepath("integrator", par.a, nu_m, "all")
    np.savez(filepath, q_arr=q_sec, p_arr=p_sec, t_arr=t_sec, step_arr=step_sec)
    print(f"Data saved in: {filepath}")

if __name__ == "__main__":
    run_integrator()
    print("Integrator run completed.")