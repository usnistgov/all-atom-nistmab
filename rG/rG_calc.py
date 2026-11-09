import pytraj as pt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


for ri in range(1,5):#5):
    traj = pt.iterload([
        '<traj_npt>_r0'+str(ri)+'.nc',
        '<traj_nvt>_r0'+str(ri)+'.nc'
    ],
        '<parm>_r0'+str(ri)+'.prmtop', mask='!(:WAT,Cl-,Na+,K+)')
    #rG
    rgdata = pt.radgyr(traj, '!(:WAT,Cl-,Na+,K+)')
    #time
    timelist = []
    for frame in traj:
        timelist.append(frame.time)
    #plot
    t = 0.001*0.001*np.array(timelist)
    r = np.array(rgdata)
    color = colors[ri - 1]
    #save
    timearray = (np.array([timelist])).T
    rgarray = (np.array([rgdata])).T
    rgWithTime = np.concatenate([timearray, rgarray], axis=1)
    np.savetxt('r0'+str(ri)+'_rg.txt', rgWithTime, delimiter='\t')

