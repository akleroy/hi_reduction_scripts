"""
Reduce M31 HI data. Runs a batch keyed off the file 'reduce-key.txt'
in the same directory. Idea is to run this iteratively, expanding the
flagging script. Only current bells-and-whistle needed should be the
possibility of antenna position corrections and delay (K-type)
calibrations.
"""

# Python imports
import os
import numpy as np
from readcol import readcol

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CONTROL FLOW
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

do_flag = False
do_calib = False
do_plotcal = False
do_apply = False
do_inspect = False
do_split = False

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DEFINITIONS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

root = "../"
reduce_key = "reduce-key.txt"
flag_script_dir = "flagging/"
mod_dir = "/usr/lib64/casapy/data/nrao/VLA/CalModels/"

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# READ THE KEY FILE
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

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
# FLAGGING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_flag
except NameError:
    do_flag = False

if do_flag:

    for ind in use[0]:
        track = track_list[ind]

        vis = root+track+"/"+track+"_hans.ms"
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        fluxcal = fluxcal_list[ind]
        cals = fluxcal+","+bpcal+","+phasecal

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

try:
    do_calib
except NameError:
    do_calib = False

if do_calib:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms"
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = fluxcal+","+bpcal+","+phasecal
        ref_ant = refant_list[ind]
        model_image = mod_dir+model_list[ind]

        print ""
        print "Calibrating "+vis
        print ""
        
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # Genearate a gain calibration table.
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        print "... generate 'gaincurve' elevation-dependent gain table."
        os.system("rm -rf "+vis+".gaincurve")
        gencal(vis=vis,
               caltable=vis+".gaincurve",
               caltype="gc")

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        # Read a model of the flux calibrator into the data
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        # ... weirdly this is the most current option for 3C48

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
                minblperant=4,
                gaintable=[vis+".gaincurve"])

        # ... apply that time correction and solve for phase & amp vs. freq

        print "... BANDPASS calibration"
        os.system("rm -rf "+vis+".bpcal")
        bandpass(vis=vis,
                 field=bpcal,
                 selectdata=False,
                 caltable=vis+'.bpcal',
                 gaincurve=False,
                 gaintable=[vis+'.bpphase',vis+".gaincurve"],
                 solint='inf,4chan',
                 combine='scan',
                 solnorm=True,
                 refant=ref_ant,
                 fillgaps=20,
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
                gaintable=[vis+'.bpcal',vis+".gaincurve"],
                gainfield=[bpcal,''],
                gaincurve=False,
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
                gaintable=[vis+'.bpcal',vis+".gaincurve"],
                gainfield=[bpcal,''],
                gaincurve=False,
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
                gaintable=[vis+'.bpcal', vis+'.intphase',vis+".gaincurve"],
                gainfield=[bpcal, '', ''],
                gaincurve=False,
                solint='inf',
                minsnr=2.0,
                minblperant=5,
                calmode='a',
                refant=ref_ant)

        # ... rescale the amplitude calibration to have true amplitude

        # ... ... save the results to a text file
        orig_logfile = casalog.logfile()
        os.system("rm -rf "+vis+".fluxscale")
        casalog.setlogfile(vis+".fluxscale")

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

        casalog.setlogfile(orig_logfile)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# INSPECT CALIBRATION TABLES
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

# Plot the calibration tables to files on disk. This step can take a
# very long time but requires no interaction. Just set it running and
# then come back and browse the PNGs.

try:
    do_plotcal
except NameError:
    do_plotcal = False

if do_plotcal:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms"
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = [fluxcal, bpcal, phasecal]
        ref_ant = refant_list[ind]

        # get the list of antennas
        tb.open(vis+"/ANTENNA")
        ant_list = tb.getcol("NAME")
        tb.close()

        # get the number of spws
        tb.open(vis+"/SPECTRAL_WINDOW")
        spw_list_in = tb.getcol("NAME")
        tb.close()        
        spw_list = []
        for i in range(len(spw_list_in)):
            spw_list.append(str(i))

        print ""
        print "Inspecting Calibration Tables for "+vis
        print ""
 
        caltable = vis+".bpphase"
        outdir = caltable+".plots/"
        os.system("rm -rf "+outdir)
        os.system("mkdir "+outdir)
        print "Short-timescale phase solution for "+track
        for ant in ant_list:
            plotcal(caltable=caltable,
                    xaxis="time",
                    yaxis="phase",
                    iteration="antenna",
                    plotrange=[0,0,-180,180],
                    plotsymbol='o', subplot=111,
                    antenna=ant,
                    figfile=outdir+"bpshort_"+ant+".png")

        caltable = vis+".bpcal"
        outdir = caltable+".plots/"
        os.system("rm -rf "+outdir)
        os.system("mkdir "+outdir)
        print "Phase/Amp vs. frequency solution for "+track
        for ant in ant_list:
            plotcal(caltable=caltable,
                    xaxis="freq",
                    yaxis="phase",
                    iteration="antenna",
                    plotrange=[0,0,-180,180],
                    plotsymbol='o', subplot=111,
                    antenna=ant,
                    figfile=outdir+"bphase_"+ant+".png")
            plotcal(caltable=caltable,
                    xaxis="freq",
                    yaxis="amp",
                    iteration="antenna",
                    plotrange=[0,0,0,0],
                    plotsymbol='o', subplot=111,
                    antenna=ant,
                    figfile=outdir+"bpamp_"+ant+".png")

        for spw in spw_list:
            plotcal(caltable=caltable,
                    xaxis="chan",
                    yaxis="amp",
                    iteration="spw",
                    plotrange=[0,0,0,0],
                    plotsymbol='o', subplot=111,
                    spw=spw,
                    figfile=outdir+"amp_vs_chan_spw"+spw+".png")                

        caltable = vis+".scanphase"
        outdir = caltable+".plots/"
        os.system("rm -rf "+outdir)
        os.system("mkdir "+outdir)
        print "Phase vs. time for "+track
        for ant in ant_list:
            plotcal(caltable=caltable,
                    xaxis="time",
                    yaxis="phase",
                    iteration="antenna",
                    plotrange=[0,0,0,0],
                    plotsymbol='o', subplot=111,
                    antenna=ant,
                    figfile=outdir+"phase_"+ant+".png")            

        caltable = vis+".scanflux"
        outdir = caltable+".plots/"
        os.system("rm -rf "+outdir)
        os.system("mkdir "+outdir)
        print "Amplitude vs. time for "+track
        for ant in ant_list:            
            plotcal(caltable=caltable,
                    xaxis="time",
                    yaxis="amp",
                    iteration="antenna",
                    plotrange=[0,0,0,0],
                    plotsymbol='o', subplot=111,
                    antenna=ant,
                    figfile=outdir+"flux_"+ant+".png")

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# APPLY CALIBRATION
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_apply
except NameError:
    do_apply = False

if do_apply:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms"
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
                 gaincurve=False,
                 gaintable=[vis+'.scanflux',
                            vis+'.scanphase',
                            vis+'.bpcal',
                            vis+'.gaincurve'],
                 gainfield=[phasecal,
                            phasecal,
                            bpcal,
                            ''],
                 calwt=False)

        print "... APPLYCAL to phase calibrator"
        applycal(vis=vis,
                 field=phasecal,
                 gaincurve=False,
                 gaintable=[vis+'.scanflux',
                            vis+'.scanphase',
                            vis+'.bpcal',
                            vis+'.gaincurve'],
                 gainfield=[phasecal,
                            phasecal,
                            bpcal,
                            ''],
                 calwt=False)

        print "... APPLYCAL to flux calibrator"
        applycal(vis=vis,
                 field=fluxcal,
                 gaincurve=False,
                 gaintable=[vis+'.scanflux',
                            vis+'.scanphase',
                            vis+'.bpcal',
                            vis+'.gaincurve'],
                 gainfield=[fluxcal,
                            fluxcal,
                            bpcal,
                            ''],
                 calwt=False)

        if (fluxcal != bpcal):
            print "... APPLYCAL to bandpass calibrator"
            applycal(vis=vis,
                     field=bpcal,
                     gaincurve=False,
                     gaintable=[vis+'.scanflux',
                                vis+'.scanphase',
                                vis+'.bpcal',
                                vis+'.gaincurve'],
                     gainfield=[phasecal,
                                phasecal,
                                bpcal,
                                ''],
                     calwt=False)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# INSPECT DATA
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_inspect
except NameError:
    do_inspect = False

if do_inspect:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms"
        source = source_list[ind]
        fluxcal = fluxcal_list[ind]
        bpcal = bpcal_list[ind]
        phasecal = phasecal_list[ind]
        cals = fluxcal+","+bpcal+","+phasecal
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
               ydatacolumn="corrected",
               field=cals)
        print "Amplitude-frequency for "+track
        ch = raw_input("Hit a key to continue.")

        plotms(vis=vis,
               xaxis="uvdist",
               yaxis="amp",
               ydatacolumn="corrected",
               avgchannel="256",
               avgtime="1e8",
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

try:
    do_split
except NameError:
    do_split = False

if do_split:

    for ind in use[0]:

        track = track_list[ind]
        vis = root+track+"/"+track+"_hans.ms"
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
