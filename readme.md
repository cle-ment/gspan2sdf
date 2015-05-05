## about

Converts graphs from a gspan dataset into sdf files. Note: Labels have to be extracted seperately or read from the gspan file.

## instructions

usage: `gspan2sdf.py [-h] -i INPUT -o OUTPUT [-a] [-b] [-v]`

* -i INPUT, --input INPUT: path to input gspan file (e.g. mydata.gspan)
* -o OUTPUT, --output OUTPUT: path to directory to store output sdf files.
* -a, --atom_shift: If this flag is set all atom labels are shifted by one, meaning e.g. an atom indexed by 0 (normally "H") would now be "He"
* -b, --bond_shift: If this flag is set the atom numbers in the bonds will be increased by one (e.g. when the labeling in gspan starts at 0 it now starts with 1 which is compliant with the sdf format
* -v, --verbose show verbose information
