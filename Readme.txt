# Author: Marcel Ruth
# Date: 01.29.21
# This script will find the best structure from gaussian output files (.out) and creates corresponding input files for gaussian16 (for cfour in the future)
-----------------------------------------------------------------
How to use:

Terminal command = python ggeometry.py folder program method basis usage

folder = Folder of the files or main folder with multiple subfolders
program = g16 (gaussian16 output files)
method = the method that you want to use e.g. B3LYP
basis = the basis set that you want to use e.g cc-pVTZ (written as "ccMinuspVTZ"
usage = opt (optimisation) or anharm (compute anharmonic frequencies)

# Abbreviations that have to be used for the method and basis flags

(Abbrev. = Result)

Kauf = (
KZu = )
Minus = -
Plus = +
Star = *
_ = /
