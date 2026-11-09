import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis as mda
#Load trajectory and create gmx ndx file with MDAnalysis
univ = mda.Universe("<path>_DIREC_REP_unwrapped.prmtop",
        "<path>_DIREC_REP_unwrapped.nc",
        format="NC")

univ.select_atoms("not (resname WAT or resname K+ or resname Cl- or resname Na+)").write("residues.ndx", name="MAB", mode="w")

numframes = len(univ.trajectory)
numframefile = open("numframes.txt", "w")
numframefile.write( str(numframes) )
numframefile.close()

#save as gromacs formats

mabonly = univ.select_atoms("resid 1:1343")
mabonly.write("PREFIX_all.xtc", frames="all")
mabonly.write("PREFIX_all.gro")
