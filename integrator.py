import numpy as np
import functions as fn
import params as par
import os
from tqdm.auto import tqdm

def run_integrator(poincare_mode="last", poincare_every=1):
    data = np.load("init_conditions/uniform_circle.npz")

    q_init = data['q']
    p_init = data['p']

    q = q_init.copy()
    p = p_init.copy()

    count = 0
    q_sec, p_sec = [], []
    q_single = None
    p_single = None

    for _ in tqdm(range(par.n_steps)):
        q += fn.Delta_q(p, par.t, par.dt/2)
        q = np.mod(q, 2 * np.pi)
        
        t_mid = par.t + par.dt/2

        p += par.dt * fn.dV_dq(q)

        q += fn.Delta_q(p, t_mid, par.dt/2)
        q = np.mod(q, 2 * np.pi)

        par.t += par.dt
        
        if np.cos(par.omega_lambda(par.t) * par.t) > 1.0-1e-5:
            if poincare_mode == "first":
                if q_single == None:
                    q_single = q.copy()
                    p_single = p.copy()
            elif poincare_mode == "last":
                #print("New section", par.t, _)
                q_single = q.copy()
                p_single = p.copy()
            elif poincare_mode == "all":
                q_sec.append(q.copy())
                p_sec.append(p.copy())
            elif poincare_mode == "number" and (count % poincare_every == 0):
                q_sec.append(q.copy())
                p_sec.append(p.copy())
                
            count += 1
    
    if poincare_mode in ["first", "last"]:
            q = q_single
            p = p_single

    elif poincare_mode in ["all", "every"]:
        if q_sec and p_sec:
            q = np.concatenate(q_sec)
            p = np.concatenate(p_sec)
        
    q = np.array(q)
    p = np.array(p)
        
# --------------- Save results -----------------

    output_dir = "integrator"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, "evolved_qp.npz")
    np.savez(file_path, q=q, p=p)

# ----------------------------------------------

if __name__ == "__main__":
    run_integrator()