"""
MBDyn Simple Pendulum - GSoC 2026 Entry Test Plot
Author: Vaibhav Sharma | March 30, 2026
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

# --- Read time steps from .out file ---
times = []
with open("pendulum.out") as f:
    for line in f:
        if line.startswith("Step "):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    times.append(float(parts[2]))
                except:
                    pass

# --- Read bob position from .mov file (node label = 1) ---
px_list, py_list, vx_list, vy_list = [], [], [], []
with open("pendulum.mov") as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 9 and parts[0] == '1':
            px_list.append(float(parts[1]))
            py_list.append(float(parts[2]))
            vx_list.append(float(parts[7]))
            vy_list.append(float(parts[8]))

# Compute angle from vertical (downward = 0 deg)
thetas = [math.degrees(math.atan2(px, -py)) for px, py in zip(px_list, py_list)]
speeds = [math.sqrt(vx**2 + vy**2) for vx, vy in zip(vx_list, vy_list)]

n = min(len(times), len(thetas))
t = np.array(times[:n])
theta = np.array(thetas[:n])
speed = np.array(speeds[:n])

# --- Analytical (small-angle) ---
g, L = 9.81, 1.0
theta0 = 30.0  # degrees
T = 2 * math.pi * math.sqrt(L / g)
t_anal = np.linspace(0, 5, 5000)
theta_anal = theta0 * np.cos(2 * math.pi / T * t_anal)

# --- Plot ---
fig, axes = plt.subplots(3, 1, figsize=(13, 10))
fig.suptitle(
    'MBDyn Simple Pendulum Simulation\n'
    'GSoC 2026 Entry Test — Vaibhav Sharma',
    fontsize=14, fontweight='bold', y=0.98
)

# Plot 1: Angle vs Time
ax = axes[0]
ax.plot(t, theta, 'b-', lw=1.5, label='MBDyn simulation', alpha=0.9)
ax.plot(t_anal, theta_anal, 'r--', lw=1.5,
        label=f'Analytical (small-angle approx, T={T:.3f} s)', alpha=0.8)
ax.axhline(0, color='k', lw=0.5, ls=':')
ax.axhline(30, color='green', lw=0.8, ls='--', alpha=0.5, label='Max angle = 30°')
ax.axhline(-30, color='green', lw=0.8, ls='--', alpha=0.5)
ax.set_xlabel('Time [s]', fontsize=11)
ax.set_ylabel('Angle θ [degrees]', fontsize=11)
ax.set_title('Pendulum Angle vs Time', fontsize=12)
ax.legend(fontsize=9, loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 5])
ax.set_ylim([-40, 40])

# Annotate period
ax.annotate(f'T = {T:.3f} s', xy=(T, theta0), xytext=(T+0.15, theta0+3),
            fontsize=9, color='darkred', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.2))

# Plot 2: Bob position (X, Y)
ax = axes[1]
ax.plot(t, px_list[:n], 'g-', lw=1.5, label='X position [m]', alpha=0.9)
ax.plot(t, py_list[:n], 'm-', lw=1.5, label='Y position [m]', alpha=0.9)
ax.axhline(-1.0, color='gray', lw=0.5, ls=':', label='Equilibrium Y = -1m')
ax.set_xlabel('Time [s]', fontsize=11)
ax.set_ylabel('Position [m]', fontsize=11)
ax.set_title('Bob Position (X and Y)', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 5])

# Plot 3: Speed vs Time
ax = axes[2]
ax.plot(t, speed, 'darkorange', lw=1.5, label='Bob speed [m/s]', alpha=0.9)
v_max = math.sqrt(2 * g * L * (1 - math.cos(math.radians(theta0))))
ax.axhline(v_max, color='red', lw=0.8, ls='--', alpha=0.7,
           label=f'Max speed at bottom = {v_max:.3f} m/s')
ax.set_xlabel('Time [s]', fontsize=11)
ax.set_ylabel('Speed [m/s]', fontsize=11)
ax.set_title('Bob Speed vs Time', fontsize=12)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 5])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('pendulum_results.png', dpi=150, bbox_inches='tight')
print("Plot saved: pendulum_results.png")
print(f"\nSimulation summary:")
print(f"  Steps: {n}")
print(f"  Duration: {t[-1]:.2f} s")
print(f"  Max angle: {max(abs(theta)):.2f}° (expected 30°)")
print(f"  Max speed: {max(speed):.4f} m/s (expected {v_max:.4f} m/s)")
print(f"  Expected period T = {T:.4f} s")
print(f"  MBDyn version: develop (compiled March 30, 2026)")
