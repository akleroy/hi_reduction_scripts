"""
Regrid the M31 data to a common velocity grid and then carry out a
UV-plane continuum subtraction. The output is suitable for
concatenation and/or direct imaging.
"""

# Python imports
import os
import numpy as np
from readcol import readcol

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CONTROL FLOW
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

do_cvel = True
do_uvcontsub = True
do_inspect = False

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# READ THE KEY FILE
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

root = "../"
reduce_key = "reduce-key.txt"

use_tag, track_in, flags_in, \
    source_in, fluxcal_in, bpcal_in, phasecal_in, \
    refant_in, model_in = \
    readcol(reduce_key, twod=False)

use = (use_tag == 'y').nonzero()
track_list = track_in
flags_list = flags_in
source_list = source_in
fluxcal_list = fluxcal_in
bpcal_list = bpcal_in
phasecal_list = phasecal_in
refant_list = refant_in
model_list = model_in

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# TUNING PARAMETERS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

vel_start = "-780km/s"
restfreq_hi = "1420.40575177MHz"
outframe = "LSRK"
vel_width = "2km/s"
phasecenter = "00h42m44.3s +41d16m09s"
nchan = 440

def_fitspw = '0:0~40,0:360~430'

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# REGRIDDING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_cvel
except NameError:
    do_cvel = False

if do_cvel:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms.split"

        print ""
        print "Regridding "+vis
        print ""

        os.system('rm -rf '+vis+'.cvel')
        cvel(vis=vis,    
             outputvis=vis+".cvel",
             mode="velocity",
             nchan=nchan,
             start=vel_start,
             width=vel_width,
             restfreq=restfreq_hi,
             phasecenter=phasecenter,
             interpolation="cubic",
             outframe=outframe)
        
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# UV CONTINUUM SUBTRACTION
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_uvcontsub
except NameError:
    do_uvcontsub = False

if do_uvcontsub:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms.split.cvel"
        source = source_list[ind]

        print ""
        print "Subtracting continuum from "+vis
        print ""

        try:
            contsub_by_field
        except NameError:
            contsub_by_field = False

        if contsub_by_field == False:

            print ""
            print "... using a single fitting window."
            print ""

            os.system('rm -rf '+vis+'.contsub')
            uvcontsub(vis=vis,             
                      field=source,
                      fitspw=def_fitspw,
                      combine='spw',
                      solint="int",
                      fitorder=0)
        else:
            print ""
            print "... using field-by-field fitting windows."
            print ""

            # Remove previous temporary files
            os.system("rm -rf "+vis+".temp_*")

            # Loop over fields
            list_to_concat = []
            for field in fit_spw_by_field.keys():

                print "... .. Field "+field

                # Split out this field
                split(vis=vis,
                      outputvis=vis+".temp_"+field,
                      field=field,
                      datacolumn="DATA")

                # Continuum subtract this field
                uvcontsub(vis=vis+".temp_"+field,
                          fitspw=fit_spw_by_field[field],
                          solint="int",
                          fitorder=0)

                # Note the file for future concatenation
                list_to_concat.append(vis+".temp_"+field+".contsub")

            # Create a single new concatenated MS
            os.system('rm -rf '+track+'.contsub')
            concat(vis=list_to_concat,
                   concatvis=vis+".contsub")  
            os.system("rm -rf "+vis+".temp_*")

