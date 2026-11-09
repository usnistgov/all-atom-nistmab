conda activate ambertools
#
directoryname="<prefix>"
directorysuffix="<suffix>"
mkdir "${directoryname}_${directorysuffix}"
cd "${directoryname}_${directorysuffix}"

for replicate in "r01" "r02" "r03" "r04"
do
	fileprefix="${directoryname}_cisf_${replicate}"
	#
	printf "\nStarting computation for ${replicate}\n"
	#CONVERT TRAJECTORY TO XTC and GRO#
	#
	#CREATE RUN TEMPLATES IN 1us INTERVALS#
	windowSize=200
	windowStride=5
	lastwindow=$(echo 10000-${windowSize} | bc)
	for starttime in $(seq 0 ${windowStride} ${lastwindow});
	do
		printf "\nStart time ${starttime} ns\n"
		endtime=$(echo ${starttime}+${windowSize} | bc) 
		startframe=$(echo 2*${starttime} | bc)
		endframe=$(echo 2*${endtime} | bc)
		for portion in "all" 
		do
			suffix="${replicate}_${portion}_s${starttime}_e${endtime}"
			#copy batch and LiquidLib input files
			cp ../run_template.sh run_${suffix}.sh
			#sed -i -e "s/DIRECTORYNAME/${directoryname}/g" run_${suffix}.sh
			sed -i -e "s/SUFFIX/${suffix}/g" run_${suffix}.sh
			cp ../cisf_gpu.in cisf_${suffix}.in
			sed -i -e "s/DIRECTORYNAME/${directoryname}/g" cisf_${suffix}.in
			sed -i -e "s/SUFFIX/${suffix}/g" cisf_${suffix}.in
			sed -i -e "s/PREFIX/${fileprefix}_${portion}/g" cisf_${suffix}.in
			sed -i -e "s/ENDFRAME/${endframe}/g" cisf_${suffix}.in
			sed -i -e "s/STARTFRAME/${startframe}/g" cisf_${suffix}.in
			frameint="1"
			sed -i -e "s/FRAMEINT/${frameint}/g" cisf_${suffix}.in 
			frameavg="1"
			sed -i -e "s/FRAMEAVG/${frameavg}/g" cisf_${suffix}.in
			trajdt="0.0005" 
			sed -i -e "s/TRAJDT/${trajdt}/g" cisf_${suffix}.in
			timeint="2"
			sed -i -e "s/TIMEINT/${timeint}/g" cisf_${suffix}.in
			timescale="linear"
			sed -i -e "s/TIMESCALE/${timescale}/g" cisf_${suffix}.in
			numtime=${windowSize}
			sed -i -e "s/NUMTIME/${numtime}/g" cisf_${suffix}.in
			sbatch run_${suffix}.sh		
		done
			#
	#time windows
	done
#replicates
done
################################################################
printf "\nEND\n_________\n"
