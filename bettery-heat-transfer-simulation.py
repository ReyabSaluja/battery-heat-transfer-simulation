import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

# --- Battery Parameters ---
rho = 2500  # Battery density (kg/m^3)
cp = 780   # Battery specific heat (J/kg.K)
k = 1.5    # Battery thermal conductivity (W/m.K)
alpha = k / (rho * cp)

# --- Battery Dimensions (m) ---
L = 0.254
H = 0.1524
D = 0.1016

# --- Grid Points (Refined for 3D) ---
nx, ny, nz = 100, 50, 25

# --- Non-Uniform Mesh Generation ---
x = np.linspace(0, L**0.8, nx)**(1/0.8)
y = np.linspace(0, H**1.2, ny)**(1/1.2)
z = np.linspace(0, D**1.2, nz)**(1/1.2)
dx, dy, dz = np.diff(x), np.diff(y), np.diff(z)
X, Y, Z = np.meshgrid(x, y, z)

# --- Initial and Boundary Conditions (in Kelvin) ---
T_initial = 298.15
T_inlet = 293.15
T_outlet = 303.15
T_amb = 298.15

# --- Convective Heat Transfer Coefficients (W/m^2.K) ---
h_coolant = 1500
h_air = 10

# --- Heat Generation Function (W/m^3) - Simplified Cycle ---
def q_dot(t):
    return 10000 + 15000 * np.sin(2 * np.pi * t / 600)**2

# --- Time Stepping and Stability ---
dt = 0.005
max_iter = 50000

# --- Convergence Criterion ---
convergence_limit = 1e-4

# --- Storage ---
T = np.full((ny, nx, nz), T_initial, dtype=float)
cpu_times = []

# --- Progress Tracking Variables ---
print_frequency = 100
last_print_time = time.time()

# --- Finite Difference Solution ---
start_time = time.time()
for iter in range(max_iter):
    T_old = T.copy()

    # Apply Boundary Conditions
    T[:, :, 0] = T_inlet + (T_outlet - T_inlet) * Y[:, :, 0] / H

    # Top, Sides, Front, & Back (Convection to Ambient)
    T[:, :, -1] = (h_air * dt * T_amb + rho * cp * dz[-1] * T_old[:, :, -1]) / (rho * cp * dz[-1] + h_air * dt)
    T[0, :, :]  = (h_air * dt * T_amb + rho * cp * dy[0]  * T_old[0, :, :])  / (rho * cp * dy[0]  + h_air * dt)
    T[:, 0, :]  = (h_air * dt * T_amb + rho * cp * dx[0]  * T_old[:, 0, :])  / (rho * cp * dx[0]  + h_air * dt)
    T[:, -1, :] = (h_air * dt * T_amb + rho * cp * dx[-1] * T_old[:, -1, :]) / (rho * cp * dx[-1] + h_air * dt)

    # Finite Difference Calculation (Interior Nodes)
    for i in range(1, nx - 1):
        for j in range(1, ny - 1):
            for k in range(1, nz - 1):
                T[j, i, k] += alpha * dt * (
                    (T_old[j, i+1, k] - 2*T_old[j, i, k] + T_old[j, i-1, k]) / dx[i]**2 +
                    (T_old[j+1, i, k] - 2*T_old[j, i, k] + T_old[j-1, i, k]) / dy[j]**2 +
                    (T_old[j, i, k+1] - 2*T_old[j, i, k] + T_old[j, i, k-1]) / dz[k]**2
                ) + q_dot(iter * dt) * dt / (rho * cp)

    # Convergence Check & Progress Update
    if np.max(np.abs(T - T_old)) < convergence_limit:
        print(f"Converged after {iter} iterations.")
        break

    # Enhanced Progress Tracking
    current_time = time.time()
    if current_time - last_print_time >= 1.0 or iter % print_frequency == 0:
        cpu_times.append(current_time - start_time)
        print(f"Iteration: {iter}, Elapsed time: {cpu_times[-1]:.2f} seconds, Max Temp: {np.max(T):.2f} K")
        last_print_time = current_time  # Update the last print time



# 3D Plotting (Example at mid-depth)
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
mid_depth_idx = nz // 2
surf = ax.plot_surface(X[:, :, mid_depth_idx], Y[:, :, mid_depth_idx],
                       T[:, :, mid_depth_idx] - 273.15, cmap='hot') # Converted to Celsius
ax.set_xlabel('Length (m)')
ax.set_ylabel('Height (m)')
ax.set_zlabel('Temperature (°C)')
plt.title('Temperature Distribution at Mid-Depth')
plt.show()