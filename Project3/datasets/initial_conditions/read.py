import numpy as np

filename = "positions_and_vel.txt"


pos = [[], [], []]
vel = [[], [], []]
with open(filename, "r") as infile:
    lines = infile.readlines()
    n = len(lines)
    for line in lines:
        vals = line.split()
        pos[0].append(float(vals[0]))
        pos[1].append(float(vals[1]))
        pos[2].append(float(vals[2]))
        vel[0].append(float(vals[3]))
        vel[1].append(float(vals[4]))
        vel[2].append(float(vals[5]))


pos = np.array(pos)
vel = np.array(vel)*365.25

outfilename = "initial_conditions_full_system.txt"

with open(outfilename, "w") as outfile:
    for i in range(n):
        l = [str(pos[0][i]), str(pos[1][i]), str(pos[2][i]), str(vel[0][i]), str(vel[1][i]), str(vel[2][i])]
        outfile.write(" ".join(l))
        outfile.write("\n")


outfilename = "initial_conditions_sun_mercury.txt"

with open(outfilename, "w") as outfile:
    l = [str(pos[0][0]), str(pos[1][0]), str(pos[2][0]), str(vel[0][0]), str(vel[1][0]), str(vel[2][0])]
    outfile.write(" ".join(l))
    outfile.write("\n")

    l = [str(pos[0][1]), str(pos[1][1]), str(pos[2][1]), str(vel[0][1]), str(vel[1][1]), str(vel[2][1])]
    outfile.write(" ".join(l))
    outfile.write("\n")

outfilename = "initial_conditions_sun_earth_jupiter.txt"

with open(outfilename, "w") as outfile:
    l = [str(pos[0][0]), str(pos[1][0]), str(pos[2][0]), str(vel[0][0]), str(vel[1][0]), str(vel[2][0])]
    outfile.write(" ".join(l))
    outfile.write("\n")

    l = [str(pos[0][3]), str(pos[1][3]), str(pos[2][3]), str(vel[0][3]), str(vel[1][3]), str(vel[2][3])]
    outfile.write(" ".join(l))
    outfile.write("\n")

    l = [str(pos[0][5]), str(pos[1][5]), str(pos[2][5]), str(vel[0][5]), str(vel[1][5]), str(vel[2][5])]
    outfile.write(" ".join(l))
    outfile.write("\n")

