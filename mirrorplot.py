""" mirrorplot
GOAL: calculate angle of mirror, depending on time of day
depending on location relative to focalpoint
AUTH: Diced
DATE: 20230325
TODO:
    - define shape
    - calculate output angle
    - calculate input angle
    - plot shape
    - plot input angles
    - plot output angles
    - plot mirrors
DONE:
    - nothing

"""
#% imports
import numpy as np
from matplotlib import pyplot as plt
from numpy import cos, sin, tan, arctan2 as atan, pi
#% constants
tau = 2*pi
todeg=180/pi
#plotbounds
xsize = 3
xmin = -1.5
xmax = xmin+xsize
ysize = 3
ymin = -0.2
ymax = ymin+ysize
x=[]
y=[]

#% function defines
def phi_in(time):
    # time in hours, starting at 6 in the morning
    # ending at 18 in the afternoon
    # 12 is in the middle
    # rate is linear I guess..
    clockfraction=(time-12)/24
    return tau*clockfraction

def phi_out(pos):
    return atan(pos,1)

def phi_mirror(time, d=-10):
    return (phi_in(time) + phi_out(d))/2

#% shape defines
def phi_corner(pos):
    #position is always at h=0
    xoff=-xmin-pos
    yoff= ysize+ymin
    print(xoff, yoff)
    return atan(xoff,yoff)

def ray(pos,hour):
    #calc incoming ray bounds
    ochtend = 0
    if hour < 12:
        msg = "laat"
        if phi_in(hour)<phi_corner(pos) and ochtend == 1:
        #calculate height
            msg = "vroeg"
        print(msg, "in de ochtend", phi_in(hour), phi_corner(pos))
    #if phi_in(hour)>phi_corner(pos) and
#% run the sucker
def main():
    t= [3]#range(6,18+1)
    d = np.linspace(xmin, xmax, 5)
    for hour in t:
        for pos in d:
            x.append(pos)
            y.append(0)
    return 1
if __name__ == '__main__':
    main()
    plt.plot(x,y,'.')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)