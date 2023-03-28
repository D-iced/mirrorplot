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

Als het goed is wel!

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
ray_in=[]

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
def ray(pos,hour):
    #calc incoming ray bounds
    #there are four bound situations
    #incoming ray before noon
    #    incoming ray, lower than top left
    #    incoming ray, highre than top left
    #incoming ray after noon
    #    incoming ray, lower than top right
    #    incoming ray, higher than top right
    #so we need to know if <= noon, and then either
    # topleft coordinates or
    # topright coordinates

    phi_r=phi_in(hour)
    print('hier', hour, pos,phi_r*todeg)
    if hour<=12:
        dx=xmin-pos
        dy=ymax
        phi_c=atan(dx,dy)
        print(phi_c*todeg)
        if phi_r < phi_c:
            xs=xmin
            ys=dx/tan(phi_r)
        else:
            xs=pos+ymax*tan(phi_r)
            ys=ymax
    else: #after noon
        dx=xmax-pos
        dy=ymax
        phi_c=atan(dx,dy)
        if phi_r > phi_c:
            xs=xmax
            ys=dx/tan(phi_r)
        else:
            xs=pos+ymax*tan(phi_r)
            ys=ymax
    #print(xs,xe,ys,ye)
    xe=pos
    ye=0
    return xs,xe,ys,ye
#% run the sucker
def main():
    t= range(6,18+1)
    d = np.linspace(xmin, xmax, 9)
    #d= [-1]
    for hour in t:
        print(phi_in(hour)*todeg)
        for pos in d:
            x.append(pos)
            y.append(0)
            #ray_in.append([xmin,pos,ymax,0])
            ray_in.append(ray(pos,hour))
    
    return 1

if __name__ == '__main__':
    main()
    #ray_in=ray_in[1:]
    for i in ray_in:
        print(f'{i}')
    plt.plot(x,y,'.')
    for ray in ray_in:
        plt.plot(ray[0:2],ray[2:])
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.show()