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
        self.x=pos
        self.angle = angle
        if pos == None:
            self.x = 0
        if angle == None:
            self.angle = (atan(self.x,1)*2-atan(self.x,1))/2
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
        self.pose=self.shape+np.array([self.x,0])
    def __repr__(self):
        return f'Mirror(x,y={self.x, self.y,}, phi={self.angle})'
    
    def update(self,angle):
        corners=self.shape
        self.angle = angle
        self.shape=[rot(corner,angle) for corner in corners]
        self.pose=self.shape+np.array([self.x,0])
    def plot(self):
        rayin = ray(self.x,self.angle)
        phi_out = atan(-self.x,1)
        rayout = ray(self.x,phi_out)
        self.update((phi_out-self.angle)/2)
        xs=[m[0] for m in self.pose]
        ys=[m[1] for m in self.pose]
        rix=rayin[0]
        riy=rayin[1]
        rox = rayout[0]
        roy = rayout[1]
        plt.plot([self.x,rox],[0,roy])
        plt.plot([rix,self.x],[riy,0])
        plt.plot(xs,ys)
        plt.gca().set_aspect('equal')
    #reflect=np.array([1,0])

#% function defines
def phi_in(time):
    # time in hours, starting at 6 in the morning
    # ending at 18 in the afternoon
    # 12 is in the middle
    # rate is linear I guess..
    clockfraction=(time-12)/24
    return tau*clockfraction


if __name__ == '__main__':
    Mlist=[]
    t = 7
    for i,v in enumerate(np.linspace(xmin+.1,xmax-.1,8)):
        Mlist.append(mirror(pos=v, angle = phi_in(t)))
        Mlist[i].plot()
    #for t in range(7,18):
    #for m in Mlist:
    #    m.update(phi_in(t))
    #    m.plot()
    #ray_in=ray_in[1:]
    #for i in ray_in:
    #    print(f'{i}')
    #plt.plot(x,y,'.')
    #for ray in ray_in:
    #    plt.plot(ray[0:2],ray[2:])
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    plt.show()