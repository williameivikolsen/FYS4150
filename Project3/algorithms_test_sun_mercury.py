'''
Test program that does the following tests:
    1) Check that solutions match with circular orbit
    2) Check that potential + kinetic energy stays constant
    3) Check that angular momentum is conserved
'''
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema  # Find local maxima
from scipy.stats import linregress

N = sys.argv[1]                         # Number of integration points
T = sys.argv[2]                         # Simulation time
path = "./results/sun_mercury"          # path to data
os.chdir(path)

filename_verlet = "Verlet_" + N + "_" + T +".txt"
# Start by reading data from files
infile_verlet = open(filename_verlet, "r")

infile_verlet.readline()                                 # Skip one line
data_verlet = np.loadtxt(filename_verlet, skiprows=4)     # Format rx-ry-vx-vy

n = int(N)
tn = float(T)
steps = np.arange(n)                                    # Arrays for plotting

def test_perihelion():     # Takes in either the data_euler or data_verlet
    print("-----------------------------------------------------------------------")
    print("Testing the precession of Mercury's orbit")
    print("-----------------------------------------------------------------------")
    rx, ry = data_verlet[:,3], data_verlet[:,4]
    radius = np.sqrt(rx*rx + ry*ry)
    perihelion_idx = argrelextrema(radius, np.less)
    deg_theta = np.arctan(ry[perihelion_idx]/rx[perihelion_idx])*180/np.pi
    print("Found {} instances of perihelion".format(len(deg_theta)))
    t_linspace = np.linspace(0, tn, len(rx))
    t = t_linspace[perihelion_idx]
    polyfit = np.polyfit(t,deg_theta, 1)
    polyval= np.polyval(polyfit, t)

    plt.plot(t[::100], deg_theta[::100], ms=1, label="Angle of pelihelion point")
    plt.plot(t[::100], polyval[::100], "r", label='Linear fit')

    plt.ylabel(r"Perihelion position, degrees from $x$-axis [$^{\circ}$]")
    plt.xlabel("Time [yr]")
    plt.legend()

    # Diagonal elements in covariant matrix are variances of coefficients in polyfit ????? RAndom guy stackexchange
    slope, intercept, r_value, p_value, std_err = linregress(t, deg_theta)
    print("Intercept linfit: {:8f}".format(intercept))
    print("Slope linfit: {:8f}".format(slope))
    print("Error slope: {:4f}".format(std_err))

    conv_factor = 100*60*60      # Deg per year to arcsec per century

    precession_per_century_arcsec = slope*conv_factor
    std_err_per_century_arcsec = std_err*conv_factor
    print("Precession per century (arcsec): {:.4f}".format(precession_per_century_arcsec))
    print("Error in slope: {:.4f}".format(std_err_per_century_arcsec))

    figname = "precession" + "N_" + N + "_T" + T + ".pdf"
    plt.tight_layout()
    plt.savefig(figname)
    plt.show()
    return None

test_perihelion()

