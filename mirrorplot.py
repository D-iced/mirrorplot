""" mirrorplot
GOAL: calculate angle of mirror, depending on time of day
depending on location relative to focalpoint
AUTH: Diced
DATE: 20230325
TODO:
    - make a single object out of a ray and mirror set
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
ysize = 1.5
ymin = -0.4
ymax = ymin+ysize
def rot(point,alpha):
    R=np.array([[np.cos(alpha), np.sin(alpha)],
                [-np.sin(alpha), np.cos(alpha)]])
    return R@point
def ray(pos,phi_r):
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


    #print('hier', hour, pos,phi_r*todeg)
    if phi_r<=0:
        dx=xmin-pos
        dy=ymax
        phi_c=atan(dx,dy)
        #print(phi_c*todeg)
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
    return xs,ys
    
class mirror:
    def __init__(self, pos=None, angle = None):
        if pos == None:
            self.pos = 0
        if angle == None:
            self.angle = 0
        self.angle = angle
        self.x=pos
        self.y=0
        w=xmax/10
        h=0.01
        base=[-w/2,w/2,-h/2,h/2] #bl corner and tr corner
        corners=[np.array([base[0],base[2]]),
                 np.array([base[0],base[3]]),
                 np.array([base[1],base[3]]),
                 np.array([base[1],base[2]]),
                 np.array([base[0],base[2]])]
        self.shape=[rot(corner,self.angle) for corner in corners]
        self.pose=self.shape+np.array([pos,0])
    def update(self):
        corners=self.shape
        self.shape=[rot(corner,self.angle) for corner in corners]
        self.pose=self.shape+np.array([pos,0])
    def plot(self):
        xs=[m[0] for m in self.pose]
        ys=[m[1] for m in self.pose]
        rayin = ray(self.x,self.angle)
        rfx=rayin[0]
        rfy=rayin[1]
        plt.plot([rfx,self.x],[rfy,0])
        plt.plot(xs,ys)
        plt.gca().set_aspect('equal')
    #reflect=np.array([1,0])
    
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
#% run the sucker
def main():
    t= range(6,18+1)
    d = np.linspace(xmin, xmax, 9)
    #d= [-1]
    for hour in t:
        #print(phi_in(hour)*todeg)
        for pos in d:
            x.append(pos)
            y.append(0)
            #ray_in.append([xmin,pos,ymax,0])
            ray_in.append(ray(pos,hour))
    
    return 1
Mlist=[]
for i,v in enumerate(np.linspace(xmin,xmax,5)):
    print(v)
    Mlist.append(mirror(pos=v,angle=v))
    Mlist[i].plot()


if __name__ == '__main__':
    main()
    #ray_in=ray_in[1:]
    #for i in ray_in:
    #    print(f'{i}')
    #plt.plot(x,y,'.')
    #for ray in ray_in:
    #    plt.plot(ray[0:2],ray[2:])
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.show()