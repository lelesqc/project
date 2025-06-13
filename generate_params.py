import yaml
import numpy as np
import os

nu_m_min = 0.8
nu_m_max = 0.9

# ---------------------------------------------

a_values = np.linspace(a_min, a_max, n_values)
nu_m_values = np.linspace(nu_m_min, nu_m_max, n_values)

output_dir = "param_grid"
os.makedirs(output_dir, exist_ok=True)

for a in a_values:
    for nu_m in nu_m_values:
        params = {
            "a": float(a_max),
            "nu_m_min": float(nu_m_min),
            "nu_m_max": float(nu_m_max)
        }
        filename = f"params_a_{a:.2f}_nu_m_{nu_m:.2f}.yaml"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            yaml.dump(params, f)
print(f"{len(a_values)*len(nu_m_values)} YAML files have been created in {output_dir}/")