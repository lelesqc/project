import numpy as np

N_PARTICLES = 50
GRID_LIM_STD = 0.05
FILENAME = "grid_conditions_standard.npz"
# ----------------------------------------------------

print("Generazione del file di condizioni iniziali standard per la griglia...")

q_0 = np.pi
p_0 = np.linspace(-GRID_LIM_STD, GRID_LIM_STD, N_PARTICLES)

q_init = np.full_like(p_0, q_0)
p_init = p_0

np.savez(FILENAME, q0=q_init, p0=p_init)

print(f"File '{FILENAME}' has been created.")
print(f"  - Number of particles: {N_PARTICLES}")
print(f"  - Grid limits: [-{GRID_LIM_STD}, {GRID_LIM_STD}]")