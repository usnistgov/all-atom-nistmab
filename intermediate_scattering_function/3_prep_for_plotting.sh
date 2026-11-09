#!/bin/sh
conda activate ambertools
#
directoryname="<prefix>"

directorysuffix="<suffix>"
cd "${directoryname}_${directorysuffix}"
#
for replicate in {1..4}; 
do
	windowSize=200
        windowStride=5
        lastwindow=$(echo 10000-${windowSize} | bc)
        for starttime in $(seq 0 ${windowStride} ${lastwindow});
	do
		for portion in "all" 
		do
			endtime=$(echo ${starttime}+${windowSize} | bc) 
		        suffix="r0${replicate}_${portion}_s${starttime}_e${endtime}"
			prefix="cisf_${suffix}"
			file="${prefix}.out"
			numKs=20
			kEnd=$(echo 2+${numKs} | bc)
			head -n $kEnd $file | tail -n $numKs  > ${prefix}_k
			fileEnd=$(wc -l < ${file})
			coordStart=$(echo ${fileEnd} - ${kEnd} - 1 | bc)
			tail -n $coordStart $file  > ${prefix}_coords
		done
	done
done
### plot
for portion in "all"
do
	cat > plot_${directoryname}_${directorysuffix}_${portion}.py <<EOF
import matplotlib.pyplot as plt
import numpy as np
	
zs = np.loadtxt('${prefix}_k')
numZs = zs.shape[0]
for r in range(1,5): #for each replicate
	plt.figure()
##############
	numFiles = len(range(0, (10000-${windowSize})+1, ${windowStride}))
	zdataIndividual = [[None]] * numFiles # (10us of 1 us increments every 250 ns for each replicate --> (1 + 9*4 = 37) )
	for i in range(numFiles): #each 1us increment
		starttime = range(0, (10000-${windowSize})+1, ${windowStride})[i]
		data = np.loadtxt("cisf_r0"+str(r)+"_${portion}_s"+str(starttime)+"_e"+str(starttime+${windowSize})+"_coords")
		t = data[:, 0]
		zdataIndividual[i] = data[:, 1:]
	zdata = np.mean(np.array(zdataIndividual), axis=0)
	
	################
	t0zdata = zdata[0, :]
	t0zdataColumn = (np.array([t0zdata])).T
	normZdata = zdata.T / t0zdataColumn
	
	cmap = plt.get_cmap('nipy_spectral')
	
	for i in range(0, numZs):
		z = normZdata[i]
		labelz = round( zs[i], 2 )
		labeldfull = (2 * np.pi) / zs[i]
		labeld = round( labeldfull, 1)
		color = cmap(i / numZs)
		plt.plot(t, z, linestyle='-', marker='o', markersize=0.01, label="Q="+str(labelz)+" nm$^{-1}$;  d="+str(labeld)+" nm", linewidth=0.6, color=color)
	plt.xlim( t[0] - (t[-1] * 0.01), t[-1] * 1.01 )
	ymin = min( min( np.ndarray.flatten(normZdata) ), 0.00001) 
	plt.ylim( 0.045, 1.05) #ymin, max( np.ndarray.flatten(normZdata) ) )
	plt.legend(labelspacing=0.001, bbox_to_anchor=(1.04, 0.5), loc="center left")
	plt.yscale('log')
	plt.xlabel('t (\$\mu\$s)')
	plt.ylabel('I(Q,t) / I(Q,0)')
	plt.savefig('${directoryname}_${directorysuffix}_${portion}_log_r0'+str(r)+'.png', dpi=500, bbox_inches="tight")
EOF
	python plot_${directoryname}_${directorysuffix}_${portion}.py
done

