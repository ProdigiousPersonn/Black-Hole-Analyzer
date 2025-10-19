import numpy as np
import matplotlib.pyplot as plt
from helpers import gravitationalRedshift, schwarzchildRadius, solarMassToKg


def plotRedshift(mass=7.2301112487166, name="Unknown Mass", minRadius=0, maxRadius=100000, sampleRate=100):
    massKg = solarMassToKg(mass)
    radii = np.linspace(minRadius, maxRadius, sampleRate)
    redshiftFactors = []
    for radius in radii:
        redshiftFactors.append(gravitationalRedshift(massKg, radius))
        
    figure = plt.figure()
    plt.plot(radii, redshiftFactors, label="Redshift Factor")
    plt.axvline(x=schwarzchildRadius(massKg), color='r', linestyle='--', label='Schwarzchild Radius/Event Horizon')
    plt.title(f"Redshift Factor (1+z) From {name} For Incremental Distances")
    plt.xlabel("Distance From Mass (m)")
    plt.ylabel("Redshift Factor (dλ∞/dλe)")
    plt.legend()
    plt.grid()
    plt.show()