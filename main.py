import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle

from constants import LIST_SIZE
from helpers import schwarzchildRadius, solarMassToKg
from time_dilation_plot import plotTimeDilation
from redshift_plot import plotRedshift
from spacetime_curve import spacetimeControls, spacetimeData
from time_animation import time_comparison_animation

mplstyle.use('fast')
plt.style.use("seaborn-v0_8-dark-palette")


dataFrame = pd.read_csv('mbh.csv', skiprows=2, header=0, sep=',')


def PrintPage(page):
    firstEntry = (page - 1) * LIST_SIZE
    lastEntry = page * LIST_SIZE
    if(page > 5):
        lastEntry = len(dataFrame['Object'])
        
    print(f"Page: {page}") 
    print("------------------")
    for i in range(firstEntry, lastEntry):
        print(f'{i + 1}: {dataFrame['Object'][i]}')
        print(f'   Mass: {dataFrame['log M_BH'][i]} \n')


awaitPageInput = True
print('View the list of black holes!\n')

while(awaitPageInput):
    page = int(input("Choose a page number (?/6):"))
    if page < 1 or page > 6:
        awaitPageInput = True
    else:
        PrintPage(page)  
        awaitPageInput = False


awaitIDInput = True
print('Choose a black hole from the list to look at!\n')
while(awaitIDInput):
    id = int(input("Choose a black hole ID (?/86):"))
    if id < 1 or id > 86:
        awaitIDInput = True
    else:
        name = dataFrame['Object'][id - 1]
        mass = float(dataFrame['log M_BH'][id - 1])
        awaitIDInput = False
print('Black Hole:', name)
print('Mass', mass)


sRadius = schwarzchildRadius(solarMassToKg(mass))
print(f"Schwarzchild radius: {sRadius}")
radius = -1
while radius < sRadius:
    if radius > 0:
        print("Radius less than schwarszchild radius!")
    radius = float(input(f"Choose a viewing radius (m) for the simulation, must be greater than the schwarszchild radius {sRadius}:"))


spacetimeData["mass"] = mass
spacetimeData["viewRadius"] = radius
spacetimeData["x0"] = radius
spacetimeData["y0"] = radius
spacetimeData["name"] = name
spacetimeControls()


plotTimeDilation(mass, name, maxRadius=radius)


plotRedshift(mass, name, maxRadius=radius)


anim = time_comparison_animation(mass)


plt.show(block=True)