import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Patch
from scipy.integrate import solve_ivp
from scipy.interpolate import RegularGridInterpolator
import matplotlib.widgets as widgets
from helpers import schwarzchildRadius, spacetimeWarp, geodesicDerivative, solarMassToKg, kgToGeometricUnit


spacetimeData = {
    "mass": 7.2301112487166,
    "viewRadius": 50000,
    "gridCount": 15,
    "plotGeodesic": True,
    "x0": 50000,
    "y0": 50000,
    "vX0": -0.1,
    "vY0": 0,
    "kappa": 0,
    "geoSamples": 2000,
    "geoDelta": 2000,
    "name": "Unknown Mass"
}


def getSpaceCurveInfo(mass, 
                      radius, 
                      lineCount, 
                      x0=0, y0=0, 
                      vX0=0, vY0=0, 
                      kappa=0, 
                      geoSamples=1000000, 
                      geoDelta=5,
                      calculateGeo=True
                      ):
    
    massKg = solarMassToKg(mass)
    massGeo = kgToGeometricUnit(massKg)

    coordinates = np.linspace(-radius, radius, lineCount)
    X, Y = np.meshgrid(coordinates, coordinates)
    
    schwarzRadius = schwarzchildRadius(massKg)
    warpFactors = spacetimeWarp(X, Y, 0, 0, massKg, schwarzRadius)
    warpFactors = np.nan_to_num(warpFactors, nan=0)
    xWarped = X * warpFactors
    yWarped = Y * warpFactors

    geodesicX = 0
    geodesicY = 0
    geodesicXWarped = 0
    geodesicYWarped = 0

    if calculateGeo:
        def geodesicSystem(time, state):
            x, yPos, vX, vY = state
            dx, dy, avX, avY = geodesicDerivative(x, yPos, vX, vY, massGeo, kappa)
            return [dx, dy, avX, avY]
        
        initialState = [x0, y0, vX0, vY0]
        tTotal = (0, geoSamples * geoDelta)
        tEvaluated = np.linspace(0, geoSamples * geoDelta, geoSamples + 1)

        geodesicSolve = solve_ivp(geodesicSystem, tTotal, initialState, t_eval=tEvaluated, method="RK45")
        geodesicX = geodesicSolve.y[0]
        geodesicY = geodesicSolve.y[1]
        geodesicWarpFactors = spacetimeWarp(geodesicX, geodesicY, 0, 0, massKg, schwarzRadius)
        geodesicXWarped = geodesicX * geodesicWarpFactors
        geodesicYWarped = geodesicY * geodesicWarpFactors
        
    return massKg, schwarzRadius, X, Y, warpFactors, xWarped, yWarped, geodesicXWarped, geodesicYWarped


def plotSpaceCurve2D(axis, 
                     massKg, 
                     schwarzRadius, 
                     X, Y, 
                     warpFactors, 
                     xWarped, yWarped, 
                     geodesicX, geodesicY, 
                     name, 
                     lineCount, 
                     plotGeodesic, 
                     plotType):
    if plotType == "radial":
        axis.plot(0, color="black", label="Spacetime Surface")
        axis.contourf(X, Y, warpFactors, levels=lineCount * 2, cmap="Greys", alpha=0.8, antialiased=False)

        axis.set_title(f"{name} (Radial)")
    
    elif plotType == "grid":
        axis.plot(0, color="black", label="Spacetime Surface")
        for i in range(lineCount):
            axis.plot(xWarped[i, :], yWarped[i, :], linewidth=1, color="black", alpha=0.3)
            axis.plot(xWarped[:, i], yWarped[:, i], linewidth=1, color="black", alpha=0.3)

        axis.set_title(f"{name} (Grid)")
        axis.legend(frameon=True, facecolor="white")
    
    if plotGeodesic:
        axis.plot(geodesicX, geodesicY, color="blue", linewidth=2, label="Geodesic Path")

    circle = Circle((0, 0), schwarzRadius, color="red", fill=False, linestyle="--", linewidth=2, label="Event Horizon", antialiased=False)
    axis.add_patch(circle)  

    axis.set_xlabel("X Plane (m)")
    axis.set_ylabel("Y Plane (m)")
    axis.legend()


def plotSpaceCurve3D(axis, 
                     massKg, 
                     schwarzRadius, 
                     X, Y, 
                     warpFactors, 
                     xWarped, yWarped, 
                     geodesicX, geodesicY, 
                     name, 
                     lineCount, 
                     plotGeodesic):
    
    axis.set_aspect("equal")
    axis.set_box_aspect(aspect=None, zoom=0.85)
    legends = [
        Patch(facecolor='gray', edgecolor='gray', label='Spacetime Surface')
    ]
    axis.plot_surface(X, Y, warpFactors, cmap=plt.cm.Greys, alpha=0.5, antialiased=False)
    
    if plotGeodesic:
        interpWarp = RegularGridInterpolator((Y[:, 0], X[0, :]), warpFactors, bounds_error=False, fill_value=0)
        points = np.vstack([geodesicY, geodesicX]).T
        zGeodesic = interpWarp(points)
        axis.plot3D(geodesicX, geodesicY, zGeodesic + 0.1, color="blue", linewidth=3,
                    label="Geodesic Path", antialiased=False)
        legends.append(Patch(facecolor='blue', edgecolor='blue', label='Geodesic Path'))

    u = np.linspace(0, 2 * np.pi, 20)
    v = np.linspace(0, np.pi, 20)
    xCircle = schwarzRadius * np.cos(u)
    yCircle = schwarzRadius * np.sin(u)
    zCircle = np.ones_like(u)
    legends.append(Patch(facecolor='red', edgecolor='red', label='Event Horizon'))
    axis.plot(xCircle, yCircle, zCircle, color="red", antialiased=False)
    
    axis.legend(handles=legends, loc='upper right')
    axis.set_zlim(0, 1)
    axis.set_xlabel("X Plane (m)")
    axis.set_ylabel("Y Plane (m)")
    axis.set_title(f"{name} (3D)")
    axis.set_zlabel(f"Spacetime Warp Factor")


def plotSpaceCurveSubplots(ax1, ax2, ax3):
    massKg, schwarzRadius, X, Y, warpFactors, xWarped, yWarped, geodesicX, geodesicY = getSpaceCurveInfo(
        spacetimeData["mass"],
        spacetimeData["viewRadius"],
        spacetimeData["gridCount"],
        spacetimeData["x0"],
        spacetimeData["y0"],
        spacetimeData["vX0"],
        spacetimeData["vY0"],
        spacetimeData["kappa"],
        spacetimeData["geoSamples"],
        spacetimeData["geoDelta"],
        spacetimeData["plotGeodesic"]
    )

    ax1.clear()
    ax2.clear()
    ax3.clear()

    plotSpaceCurve2D(ax1, massKg, schwarzRadius, X, Y, warpFactors, xWarped, yWarped, geodesicX, geodesicY, spacetimeData["name"], spacetimeData["gridCount"], spacetimeData["plotGeodesic"], "radial")
    plotSpaceCurve2D(ax2, massKg, schwarzRadius, X, Y, warpFactors, xWarped, yWarped, geodesicX, geodesicY, spacetimeData["name"], spacetimeData["gridCount"], spacetimeData["plotGeodesic"], "grid")
    plotSpaceCurve3D(ax3, massKg, schwarzRadius, X, Y, warpFactors, xWarped, yWarped, geodesicX, geodesicY, spacetimeData["name"], spacetimeData["gridCount"], spacetimeData["plotGeodesic"])


def spacetimeControls():
    figure = plt.figure(figsize=(12, 7))
    figure.suptitle("Spacetime Curvature Visualization", fontsize=24, fontweight='bold')
    ax1 = figure.add_subplot(1, 3, 1)
    ax2 = figure.add_subplot(1, 3, 2)
    ax3 = figure.add_subplot(1, 3, 3, projection='3d')
    ax1.set_aspect('equal', 'box')
    ax2.set_aspect('equal', 'box')

    figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.25, wspace=0.15)

    axisRadius = plt.axes([0.15, 0.20, 0.7, 0.03])
    axisx0 = plt.axes([0.15, 0.15, 0.7, 0.03])
    axisy0 = plt.axes([0.15, 0.10, 0.7, 0.03])
    axisvx0 = plt.axes([0.15, 0.05, 0.7, 0.03])
    axisvy0 = plt.axes([0.15, 0.00, 0.7, 0.03])

    sliderRadius = widgets.Slider(axisRadius, "Viewing Radius (m)", 0, spacetimeData["viewRadius"]+500000,
                          valinit=spacetimeData["viewRadius"], valfmt='%d', facecolor='blue')
    sliderx0 = widgets.Slider(axisx0, "X0 (m)", 0, spacetimeData["viewRadius"],
                      valinit=spacetimeData["x0"], valfmt='%d', facecolor='green')
    slidery0 = widgets.Slider(axisy0, "Y0 (m)", 0, spacetimeData["viewRadius"],
                      valinit=spacetimeData["y0"], valfmt='%d', facecolor='green')
    slidervx0 = widgets.Slider(axisvx0, "vX0 (m/s)", -5, 5,
                       valinit=spacetimeData["vX0"], valfmt='%.2f', facecolor='red')
    slidervy0 = widgets.Slider(axisvy0, "vY0 (m/s)", -5, 5,
                       valinit=spacetimeData["vY0"], valfmt='%.2f', facecolor='red')

    def updatePlot(event=None):
        spacetimeData["viewRadius"] = int(sliderRadius.val)
        spacetimeData["x0"] = int(sliderx0.val)
        spacetimeData["y0"] = int(slidery0.val)
        spacetimeData["vX0"] = float(slidervx0.val)
        spacetimeData["vY0"] = float(slidervy0.val)
        plotSpaceCurveSubplots(ax1, ax2, ax3)
        figure.canvas.draw_idle()

    sliderRadius.on_changed(lambda val: updatePlot(val)) 
    sliderx0.on_changed(lambda val: updatePlot(val)) 
    slidery0.on_changed(lambda val: updatePlot(val)) 
    slidervx0.on_changed(lambda val: updatePlot(val)) 
    slidervy0.on_changed(lambda val: updatePlot(val))

    plt.ion()
    plotSpaceCurveSubplots(ax1, ax2, ax3)
    plt.show(block=False)