import numpy as np
import matplotlib.pyplot as plt
from helpers import schwarzchildDilation, schwarzchildRadius, solarMassToKg


def plotTimeDilation(mass=7.2301112487166, name="Unknown Mass", minRadius=0, maxRadius=100000, sampleRate=100):
    massKg = solarMassToKg(mass)
    radii = np.linspace(minRadius, maxRadius, sampleRate)
    dilationFactors = []
    for radius in radii:
        dilationFactors.append(schwarzchildDilation(massKg, radius))
        
    figure = plt.figure()
    plt.plot(radii, dilationFactors, label="Time Dilation Factor")
    plt.axvline(x=schwarzchildRadius(massKg), color='r', linestyle='--', label='Schwarzchild Radius/Event Horizon')
    plt.title(f"Time Dilation Factor From {name} For Incremental Distances")
    plt.xlabel("Distance From Mass (m)")
    plt.ylabel("Time Dilation Factor (dtr/dt∞)")
    plt.legend()
    plt.grid()
    plt.show(block=False)