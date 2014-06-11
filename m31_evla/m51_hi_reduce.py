"""
Reduce M51 HI data.
"""

# Python imports
import os
import numpy as np
from readcol import readcol

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CONTROL FLOW
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

do_flag = True
do_calib = True
do_inspectcal = False
do_apply = True
do_inspect = True
do_split = False
# do_cvel = False
do_plotcontsub = False
do_contsub = False

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DEFINITIONS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

root = "../"
reduce_key = "reduce-key.txt"
flag_script_dir = "flagging/"
mod_dir = "/usr/lib64/casapy/data/nrao/VLA/CalModels/"
fitspw = ""

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# READ THE KEY FILE
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

use_tag, track_in, flags_in, \
         source_in, fluxcal_in, bpcal_in, phasecal_in, \
         refant_in, model_in = \
         readcol(reduce_key, twod=False, skipline=6)

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
# FLAGGING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_flag
except NameError:
    do_flag = False

if do_flag:

    for ind in use[0]:
        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms"
        flag_script = flag_script_dir+flags_list[ind]
        
        print ""
        print "Flag reset and flagging script for "+track
        print ""

        print "... reseting flags."

        flagmanager(vis=vis,
                    mode="restore",
                    versionname="Original")

        print "... executing track specific flagging."
        
        execfile(flag_script)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CALIBRATION
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_calib:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms"
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = fluxcal+","+bpcal+","+phasecal
        ref_ant = refant_list[ind]
        model_image = mod_dir+model_list[ind]

        print ""
        print "Calibrating "+vis
        print ""
        
        # Read a model of the flux calibrator into the data

        print "... SETJY on fluxcal"
        setjy(vis=vis, 
              field=fluxcal, 
              modimage=model_image,
              standard="Perley-Butler 2010")

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # Calibrate the bandpass (amp/phase response of antennas vs. frequency)
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        # ... solve for short-timescale phase variability

        print "... a short phase GAINCAL on the bandpass calibrator."
        os.system("rm -rf "+vis+".bpphase")
        gaincal(vis=vis,
                field=bpcal,
                caltable=vis+'.bpphase',
                refant=ref_ant,
                calmode='p',
                solint='int',
                minsnr=2.0,
                minblperant=4)

        # ... apply that time correction and solve for phase & amp vs. freq

        print "... BANDPASS calibration"
        os.system("rm -rf "+vis+".bpcal")
        bandpass(vis=vis,
                 field=bpcal,
                 selectdata=False,
                 caltable=vis+'.bpcal',
                 gaincurve=True,
                 gaintable=[vis+'.bpphase'],
                 solint='inf',
                 combine='scan',
                 solnorm=True,
                 refant=ref_ant,
                 bandtype='B')

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # Calibrate the phase and amp vs. time
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        # ... solve for the phase vs. time (per scan)

        print "... a phase GAINCAL (per scan)"
        os.system("rm -rf "+vis+'.scanphase')
        gaincal(vis=vis,
                field=cals,
                selectdata=True,
                caltable=vis+'.scanphase',
                append=False,
                gaintable=[vis+'.bpcal'],
                gainfield=[bpcal],
                gaincurve=True,
                calmode='p',
                solint='inf',
                minsnr=2.0,
                minblperant=4,
                refant=ref_ant)
        
        # ... phase vs. time (integration) to help with amplitude cal

        print "... a phase GAINCAL (per integration)"
        os.system("rm -rf "+vis+".intphase")
        gaincal(vis=vis,
                field=cals,
                selectdata=True,
                caltable=vis+'.intphase',
                append=False,
                gaintable=[vis+'.bpcal'],
                gainfield=[bpcal],
                gaincurve=True,
                calmode='p',
                solint='int',
                minsnr=2.0,
                minblperant=4,
                refant=ref_ant)

        # ... amp vs. time (per scan)

        print "... an amplitude GAINCAL (per scan)"
        os.system("rm -rf "+vis+".scanamp")
        gaincal(vis=vis,
                field=cals,
                selectdata=True,
                caltable=vis+'.scanamp',
                append=False,
                gaintable=[vis+'.bpcal', vis+'.intphase'],
                gainfield=[bpcal, ""],
                gaincurve=True,
                solint='inf',
                minsnr=2.0,
                minblperant=5,
                calmode='a',
                refant=ref_ant)

        # ... rescale the amplitude calibration to have true amplitude

        print "... FLUXSCALE on the amplitude gaincal"
        os.system("rm -rf "+vis+".scanflux")
        if (fluxcal != bpcal):
            transfer = phasecal+','+bpcal
        else:
            transfer = phasecal
        fluxscale(vis=vis,
                  caltable=vis+'.scanamp',
                  fluxtable=vis+'.scanflux',
                  transfer=transfer,
                  reference=fluxcal)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# INSPECT CALIBRATION TABLES
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_inspectcal:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms"
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        print ""
        print "Inspecting Calibration Tables for "+vis
        print ""

        caltable = vis+".bpphase"
        plotcal(caltable=caltable,
                xaxis="time",
                yaxis="phase",
                iteration="antenna",
                plotrange=[0,0,-180,180],
                plotsymbol='o', subplot=331)
        print "Short-timescale phase solution for "+track
        ch = raw_input("Hit a key to continue.")

        caltable = vis+".bpcal"
        plotcal(caltable=caltable,
                xaxis="freq",
                yaxis="phase",
                iteration="antenna",
                plotrange=[0,0,-180,180],
                plotsymbol='o', subplot=331)
        print "Phase vs. frequency solution for "+track
        ch = raw_input("Hit a key to continue.")

        caltable = vis+".bpcal"
        plotcal(caltable=caltable,
                xaxis="freq",
                yaxis="amp",
                iteration="antenna",
                plotrange=[0,0,0,0],
                plotsymbol='o', subplot=331)
        print "Amplitude vs. frequency for "+track
        ch = raw_input("Hit a key to continue.")

        caltable = vis+".scanphase"
        plotcal(caltable=caltable,
                xaxis="time",
                yaxis="phase",
                iteration="antenna",
                plotrange=[0,0,0,0],
                plotsymbol='o', subplot=331)
        print "Phase vs. time for "+track
        ch = raw_input("Hit a key to continue.")

        caltable = vis+".scanflux"
        plotcal(caltable=caltable,
                xaxis="time",
                yaxis="amp",
                iteration="antenna",
                plotrange=[0,0,0,0],
                plotsymbol='o', subplot=331)
        print "Amplitude vs. time for "+track
        ch = raw_input("Hit a key to continue.")

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# APPLY CALIBRATION
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_apply:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms"
        source = source_list[ind]
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        print ""
        print "Applying calibration to "+vis
        print ""

        print "... APPLYCAL to source"
        applycal(vis=vis,
                 field=source,
                 gaincurve=True,
                 gaintable=[vis+'.scanflux',
                            vis+'.scanphase',
                            vis+'.bpcal'],
                 interp="linear,linear",
                 gainfield=[phasecal,
                            phasecal,
                            bpcal],
                 calwt=False)

        print "... APPLYCAL to phase calibrator"
        applycal(vis=vis,
                 field=phasecal,
                 gaincurve=True,
                 gaintable=[vis+'.scanflux',
                            vis+'.scanphase',
                            vis+'.bpcal'],
                 interp="linear,linear",
                 gainfield=[phasecal,
                            phasecal,
                            bpcal],
                 calwt=False)

        print "... APPLYCAL to flux calibrator"
        applycal(vis=vis,
                 field=fluxcal,
                 gaincurve=True,
                 gaintable=[vis+'.scanflux',
                            vis+'.scanphase',
                            vis+'.bpcal'],
                 interp="linear,linear",
                 gainfield=[fluxcal,
                            fluxcal,
                            bpcal],
                 calwt=False)

        if (fluxcal != bpcal):
            print "... APPLYCAL to bandpass calibrator"
            applycal(vis=vis,
                     field=bpcal,
                     gaincurve=True,
                     gaintable=[vis+'.scanflux',
                                vis+'.scanphase',
                                vis+'.bpcal'],
                     interp="linear,linear",
                     gainfield=[phasecal,
                                phasecal,
                                bpcal],
                     calwt=False)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# INSPECT DATA
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_inspect:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms"
        source = source_list[ind]
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        print ""
        print "Inspecting Data for "+vis
        print ""
    
        plotms(vis=vis,
               iteraxis="field",
               xaxis="frequency",
               yaxis="amp",
               avgtime="1e8",
               averagedata=True,
               avgscan=T,
               ydatacolumn="corrected")
        print "Amplitude-frequency for "+track
        ch = raw_input("Hit a key to continue.")

        plotms(vis=vis,
               xaxis="uvdist",
               yaxis="amp",
               ydatacolumn="corrected",
               avgchannel="256",
               averagedata=True,
               field=phasecal)
        print "Amplitude-uvdist for "+track
        ch = raw_input("Hit a key to continue.")

        plotms(vis=vis,
               xaxis="time",
               yaxis="amp",
               ydatacolumn="corrected",
               avgchannel="256",
               averagedata=True,
               coloraxis="field")
        print "Amplitude-time for "+track
        ch = raw_input("Hit a key to continue.")

	default(plotms)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# SPLIT
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_split:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms"
        source = source_list[ind]
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        print ""
        print "Splitting calibrated data for "+vis
        print ""

        os.system('rm -rf '+vis+'.split')
        split(vis=vis,
              outputvis=vis+'.split',
              field=source,
              datacolumn='corrected',
              keepflags=False)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DO FREQUENCY REGRIDDING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

#if do_cvel:
#
#    for ind in use[0]:
#
#        track = track_list[ind]
#        vis = root+track+"/"+track+"_hi_hans.ms.split"
#        source = source_list[ind]
#        fluxcal = fluxcal_list[ind]
#        bpcal = bpcal_list[ind]
#        phasecal = phasecal_list[ind]
#        cals = [fluxcal, bpcal, phasecal]
#        ref_ant = ref_ant[ind]
#
#        print ""
#        print "Regridding spectral windows for "+vis
#        print ""
#
#        os.system('rm -rf '+vis+'.cvel')
#        cvel(vis=vis,    
#             outputvis=vis+".cvel",
#             mode="velocity",
#             nchan=-1,
#             start=0,
#             width=1,
#             restfreq="1420.40575177MHz",
#             outframe="LSRK")

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# UV CONTINUUM SUBTRACTION
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_plotcontsub:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms.split" #.cvel"
        source = source_list[ind]
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        print ""
        print "Plotting amp. vs. chan for "+vis
        print ""

        plotms(vis=vis,              
               field=source,
               xaxis='chan',
               yaxis='amp',
               avgtime='1e8s',
               avgscan=True,
               avgbaseline=True)

if do_contsub:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hi_hans.ms.split" #".cvel"
        source = source_list[ind]
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        print ""
        print "Subtracting continuum from "+vis
        print ""

        os.system('rm -rf '+vis+'.contsub')
        uvcontsub(vis=vis,             
                  field=source,
                  fitspw=fitspw,
                  combine='spw',
                  solint="int",
                  fitorder=0)            
