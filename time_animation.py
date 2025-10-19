import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from constants import GRAV_CONST, LIGHT_SPEED
from helpers import solarMassToKg


def time_comparison_animation(mass):
    plt.rcParams["animation.html"] = "jshtml"
    plt.rcParams['figure.dpi'] = 150  

    mass_kg = solarMassToKg(mass)

    Rs = 2 * GRAV_CONST * mass_kg / LIGHT_SPEED**2

    tau_values = np.linspace(0.1, 20, 200)

    radii_values = np.linspace(20 * Rs, 1.001 * Rs, 200)

    def dilated_time(tau, r, Rs):
        factor = np.sqrt(1 - Rs / r)
        return tau / factor

    fig, ax = plt.subplots(figsize=(8, 5))

    def animate(i):
        ax.cla()
        tau = tau_values[i]
        r = radii_values[i]
        dt = dilated_time(tau, r, Rs)
        
        trace_tau = tau_values[:i+1]
        trace_dt = [dilated_time(tau_values[j], radii_values[j], Rs) for j in range(i+1)]

        ax.plot(trace_tau, trace_dt, 'r:', alpha=0.6)
        ax.plot(tau, dt, 'ro')

        ax.set_xlim(0, tau_values[-1] * 1.2)
        max_dt = dilated_time(tau_values[-1], radii_values[-1], Rs) * 1.2
        ax.set_ylim(0, max_dt)
        ax.set_xlabel('Proper Time (s)')
        ax.set_ylabel('Dilated Time (s)')
        ax.set_title('Dilated Time vs Proper Time as Distance to Black Hole Decreases')
        ax.grid(True)
        ax.text(0.5, 1.07,
                f'Radius: {r/Rs:.3f} Rs  |  Proper Time: {tau:.2f} s | Dilated Time: {dt:.2f} s',
                transform=ax.transAxes, ha='center')

    ani = animation.FuncAnimation(fig, animate, frames=len(tau_values),
                                interval=100, repeat=True)
    
    plt.show()
    
    return ani