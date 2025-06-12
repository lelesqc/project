import os

def get_output_filepath(filename, a, nu_m):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    param_str = f"a_{a:.2f}_nu_m_{nu_m:.2f}"
    filepath = os.path.join(data_dir, f"{filename}_{param_str}.npz")
    return filepath
