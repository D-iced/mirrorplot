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
def ray(pos):
    #calc incoming ray bounds
        

#% run the sucker
def main():
    x=[]
    y=[]
    t=range(6,18+1)
    for hour in t:
        print(phi_mirror(hour,0)*todeg)
        x.append((phi_mirror(hour,0)*todeg))
        y.append(hour)
    print(x)
    print(y)
    plt.plot(x,y)
    plt.show()
    return 1
if __name__ == '__main__':
    main()