import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis as mda
import MDAnalysis.analysis.msd as msd
#Load trajectory and create gmx ndx file with MDAnalysis
univ = mda.Universe("../unwrapped/aa_NISTmAb_water_PREFIX_REP_unwrapped.prmtop", "../unwrapped/aa_NISTmAb_water_PREFIX_REP_unwrapped.nc", format="NC")

print("running center atom")
centeratomMSD = msd.EinsteinMSD( univ, select="(resid 892) and (name SG) and (resname CYX)", msd_type='xyz', fft=True)
centeratomMSD.run()
centeratomMsdData = centeratomMSD.results.timeseries
np.savetxt("/lab/mml/kipp/645div/nistmab/analysis/diffusion/data_output_txt_files/mda_centeratom_msd_PREFIX_REP.txt", centeratomMsdData)

print("running CoM")
comMSD = msd.EinsteinMSD( univ, select="resid 1:1343", msd_type='xyz', fft=True)
comMSD.run()
comMsdData = comMSD.results.timeseries
np.savetxt("/lab/mml/kipp/645div/nistmab/analysis/diffusion/data_output_txt_files/mda_com_msd_PREFIX_REP.txt", comMsdData)

print("running water")
watMSD = msd.EinsteinMSD( univ, select="(resname WAT)", msd_type='xyz', fft=True)
watMSD.run()
watMsdData = watMSD.results.timeseries
np.savetxt("/lab/mml/kipp/645div/nistmab/analysis/diffusion/data_output_txt_files/mda_wat_msd_water_PREFIX_REP.txt", watMsdData)

###
###
nframes = centeratomMSD.n_frames
print("_____ nframes = "+str(nframes)+" frames __________")
exit()



timestep = 0.001*(0.05*10) # this needs to be the actual time between frames
lagtimes = np.arange(nframes)*timestep # make the lag-time axis
#############
fig = plt.figure()
ax = plt.axes()
#
exactpt6 = lagtimes*0.6
exact1pt5 = lagtimes*1.5
exact3 = lagtimes*3.0
exact6 = lagtimes*6.0
exact15 = lagtimes*15
exact30 = lagtimes*30
exact60 = lagtimes*60
exact2036 = lagtimes*2.03*60
exact22360 = lagtimes*2.23*600
exact22760 = lagtimes*2.27*600
# plot the exact result
#ax.plot(lagtimes, exact2036, ls="--", label=r'Forcefield WT4 D = $2.03 x 10^{-6}$ cm$^2$/s', color='deepskyblue')
#ax.plot(lagtimes, exact22360, ls="--", label=r'Forcefield water D = $2.23 x 10^{-5}$ cm$^2$/s', color='blue')
ax.plot(lagtimes, exact22760, ls="--", label=r'Experimental water D = $2.27 x 10^{-5}$ cm$^2$/s', color='navy')
#water
#
ax.plot(lagtimes, exact60, ls="--", label=r'$y=60\tau$, D = $1 x 10^{-6}$ cm$^2$/s', color='lightgray')
ax.plot(lagtimes, exact30, ls=":", label=r'$y=30\tau$, D = $5 x 10^{-7}$ cm$^2$/s', color='black')
ax.plot(lagtimes, exact15, ls=":", label=r'$y=15\tau$, D = $2.5 x 10^{-7}$ cm$^2$/s', color='gray')
ax.plot(lagtimes, exact6, ls=":", label=r'$y=6\tau$, D = $1 x 10^{-7}$ cm$^2$/s', color='lightgray')
ax.plot(lagtimes, exact3, ls="-.", label=r'$y=3\tau$, D = $5 x 10^{-8}$ cm$^2$/s', color='black')
ax.plot(lagtimes, exact1pt5, ls="-.", label=r'$y=1.5\tau$, D = $2.5 x 10^{-8}$ cm$^2$/s', color='gray')
ax.plot(lagtimes, exactpt6, ls="-.", label=r'$y=0.6\tau$, D = $1 x 10^{-8}$ cm$^2$/s', color='lightgray')
#
# plot the actual MSD
ax.plot(lagtimes, 0.001*watMsdData, ls="-", label=r'Water', color='deepskyblue')
#
ax.plot(lagtimes, 0.001*comMsdData, ls="-", label=r'Entire NISTmAb CoM', color='peru')
ax.plot(lagtimes, 0.001*centeratomMsdData, ls="-", label=r'Hinge BSG bead', color='yellow')
#
#
#plt.ylim(0, 200)#1.4 * max( np.ndarray.flatten(lc1MsdData) ) )
plt.xlabel('time [$\mu$s]')
plt.ylabel('MSD')
plt.legend(labelspacing=0.1, bbox_to_anchor=(1.04, 0.5), loc="center left")
plt.savefig('mda_msd_paper_PREFIX_REP.png', dpi=500, bbox_inches="tight")
##########################################
##########################################
exit()

