import numpy as np
from constants import GRAV_CONST, LIGHT_SPEED, SOLAR_MASS_KG


def schwarzchildRadius(mass):
    return (2*GRAV_CONST*mass)/(LIGHT_SPEED**2)


def schwarzchildDilation(mass, radius):
    radLimit = schwarzchildRadius(mass)
    if radius < radLimit: 
        return 0 
    return np.sqrt(1-(radLimit/radius))


def gravitationalRedshift(mass, radius):
    radLimit = schwarzchildRadius(mass)
    if radius < radLimit: 
        return 0 
    return (np.sqrt(1-(radLimit/radius)))**(-1)


def spacetimeWarp(x, y, gX, gY, mass, radius):
    radialCoord = np.sqrt((x - gX)**2 + (y - gY)**2)
    with np.errstate(divide='ignore', invalid='ignore'):
        warpFactor = np.sqrt(1 - radius / radialCoord)
    return warpFactor


def solarMassToKg(mass):
    return mass * SOLAR_MASS_KG


def coordinateToRadius(x, y):
    return np.sqrt(x**2 + y**2)


def calculateAngularVelocity(x, y, vX, vY):
    radius = coordinateToRadius(x,y)
    if radius < 1e-10:
        return 0
    return (x*vY - y*vX) / (radius**2)


def geodesicDerivative(x, y, vX, vY, mass, kappa=0):
    radius = coordinateToRadius(x, y)
    if radius < 1e-10:
        return 0, 0, 0, 0
    angularVelocity = calculateAngularVelocity(x, y, vX, vY)
    accelCoeff = (mass * kappa) / (radius**2) - (3 * mass * angularVelocity**2) / radius
    dx = vX
    dy = vY
    avX = x * accelCoeff
    avY = y * accelCoeff
    
    return dx, dy, avX, avY


def kgToGeometricUnit(mass):
    return GRAV_CONST * mass / LIGHT_SPEED**2
    

def properTime(t, mass, radius):
    T0 = t * schwarzchildDilation(mass, radius)
    return T0


def redshiftedWavelength(wavelengthEmit, mass, radius):
    wavelengthInf = wavelengthEmit * gravitationalRedshift(mass, radius)