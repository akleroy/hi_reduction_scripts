"""
This script imports data and creates the directory structure for
the M31 EVLA project.
"""

# Python imports
import os
import numpy as np
from readcol import readcol

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CONTROL FLOW
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

do_makedir = True
do_copy = True
do_listobs = True
do_hanning = True
do_flag = True

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DEFINITIONS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

root = "../"
sb_key = "sb_key.txt"

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# READ THE SCHEDULING BLOCK KEY
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

msname_in, config_in, name_in, \
    dir_in, use_tag = \
    readcol(sb_key, twod=False, skipline=5)

use = (use_tag == 'y').nonzero()
msname = msname_in
config = config_in
name = name_in
directory = dir_in

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# IF REQUESTED, MAKE THE DIRECTORY STRUCTURE
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_makedir
except NameError:
    do_makedir = False

if do_makedir:
    for ind in use[0]:
        os.system("mkdir "+root+name[ind])

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# COPY DATA
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_copy
except NameError:
    do_copy = False

if do_copy:
        print "Removing old data and copying MS"
    for ind in use[0]:
        infile = directory[ind]+msname[ind]
        outfile = root+name[ind]+"/"+name[ind]+".ms"
        print "... copying "+infile+" to "+outfile
        os.system('rm -rf '+outfile)
        os.system('cp -r '+infile+' '+outfile)                        

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# LISTOBS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_listobs
except NameError:
    do_listobs = False

if do_listobs:
    for ind in use[0]:
        msfile = root+name[ind]+"/"+name[ind]+".ms"
        listfile = msfile+".listobs"
        listobs(msfile, listfile=listfile)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# HANNING SMOOTHING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_hanning
except NameError:
    do_hanning = False

if do_hanning:
    print "Hanning smoothing data."
    for ind in use[0]:
        infile = root+name[ind]+"/"+name[ind]+".ms"
        outfile = root+name[ind]+"/"+name[ind]+"_hans.ms"

        os.system('rm -rf '+outfile+'.temp')
        hanningsmooth(vis=infile,
                      datacolumn='data',
                      outputvis=outfile+'.temp')
        os.system('rm -rf '+outfile)
        split(vis=outfile+'.temp',
              datacolumn='data',
              outputvis=outfile,
              width=2,
              correlation='RR,LL',
              keepflags=False)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# FLAGGING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_flag
except NameError:
    do_flag = False

if do_flag:
    print "Flagging"
    for ind in use[0]:
        infile = root+name[ind]+"/"+name[ind]+"_hans.ms"

        print "... flagging shadowed data."
        flagdata(vis=infile,
                 mode="shadow",
                 flagbackup=False)

        os.system("rm -rf "+infile+".flagversions")
        flagmanager(vis=infile,
                    mode="save",
                    versionname="Original")

