from readcol import readcol
import os

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# ASSEMBLE THE TRACK LIST
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

ms_name, ms_config, ms_track = readcol(ms_key, twod=False, skipline=3)
use = ((ms_config == use_config)*(ms_track == use_track)).nonzero()
temp = list(ms_track[use[0]])
track_list = []
for track in temp:
    track_list.append(track+'.ms')

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# COPY RAW DATA
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_copy
except NameError:
    do_copy = False

if do_copy:
    # delete previous version and copy
    for ind in use[0]:
        print "Removing old data and recopying new MS"
        os.system('rm -rf '+ms_track[ind]+'.ms')
        os.system('cp -r '+data_dir+ms_name[ind]+' '+ ms_track[ind]+'.ms')

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# LISTOBS
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_list
except NameError:
    do_list = False

if do_list:
    for track in track_list:
        os.system('rm -rf '+track+'.listobs')
        listobs(vis=track, listfile=track+'.listobs')

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# SMOOTHING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

try:
    do_smooth
except NameError:
    do_smooth = False

if do_smooth:
    print "Smoothing data."
    for track in track_list:
        os.system('rm -rf '+track+'.hans')
        hanningsmooth(vis=track,
                      datacolumn='data',
                      outputvis=track+'.hans')
        os.system('rm -rf '+track+'.smooth')
        split(vis=track+'.hans',
              datacolumn='data',
              outputvis=track+'.smooth',
              spw=use_spw,
              timebin=timebin,
              width=width,
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
    # Do basic flagging
    for track in track_list:
        print ""
        print "Flag reset and autoflagging for "+track
        print ""

        vis = track+'.smooth'

        print "... reseting flags."
        flagdata(vis=vis,
                 unflag=True,
                 flagbackup=False)
        print "... flagging autocorrelations."
        flagdata(vis=vis,
                 autocorr=True,
                 flagbackup=False)
        print "... flagging shadowed data."
        flagdata(vis=vis,
                 mode="shadow",
                 flagbackup=False)
        print "... flagging edge channels."
        flagdata(vis=vis,
                 spw=edge_chan,
                 flagbackup=False)

    # Execute track-specific flagging
    execfile(flag_script)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CALIBRATE
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_calib:
    for track in track_list:
        print ""
        print "Calibrating "+track
        print ""

        vis = track+'.smooth'

        # Read a model of the flux calibrator into the data

        print "... SETJY on fluxcal"
        setjy(vis=vis, 
              field=fluxcal, 
              modimage=model_image,
              standard="Perley-Butler 2010")

        # Calibrate the bandpass (amp/phase response of antennas vs. frequency)

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

        # Calibrate the phase and amp vs. time

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
                gaintable=vis+'.bpcal',
                gainfield=bpcal,
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
                gainfield=[bpcal, cals],
                gaincurve=gaincurvecal,
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

    for track in track_list:

        vis = track+'.smooth'

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

    for track in track_list:

        vis = track+'.smooth'

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
                 interp=interpmode,
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
                 interp=interpmode,
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
                 interp=interpmode,
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
                     interp=interpmode,
                     gainfield=[phasecal,
                                phasecal,
                                bpcal],
                     calwt=False)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# INSPECT DATA
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_inspect:

    for track in track_list:

        vis = track+'.smooth'

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

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# SPLIT
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_split:

    for track in track_list:

        vis = track+'.smooth'

        print ""
        print "Splitting calibrated data for "+vis
        print ""

        os.system('rm -rf '+track+'.split')
        split(vis=vis,
              outputvis=track+'.split',
              field=source,
              datacolumn='corrected',
              keepflags=False)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# DO FREQUENCY REGRIDDING
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_cvel:

    for track in track_list:

        vis = track+'.split'

        print ""
        print "Regridding spectral windows for "+vis
        print ""

        os.system('rm -rf '+vis+'.cvel')
        cvel(vis=vis,    
             outputvis=vis+".cvel",
             mode="velocity",
             nchan=-1,
             start=0,
             width=1,
             restfreq="1420.40575177MHz",
             phasecenter=phasecenter)

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# UV CONTINUUM SUBTRACTION
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_plotcontsub:

    for track in track_list:

        vis = track+'.split.cvel'

        print ""
        print "Subtracting continuum from "+vis
        print ""

        plotms(vis=vis,              
               field=source,
               xaxis='chan',
               yaxis='amp',
               avgtime='1e8s',
               avgscan=True,
               avgbaseline=True)

if do_contsub:

    for track in track_list:
        
        vis = track+'.split.cvel'

        print ""
        print "Subtracting continuum from "+vis
        print ""

        if contsub_by_field == False:
            os.system('rm -rf '+vis+'.contsub')
            uvcontsub(vis=vis,             
                      field=source,
                      fitspw=fitspw,
                      combine='spw',
                      solint="int",
                      fitorder=0)
        else:
            print ""
            print "Using field-by-field SPWs."
            print ""
            os.system("rm -rf "+vis+".temp_*")
            list_to_concat = []
            for field in fit_spw_by_field.keys():
                print "... Field "+field
                split(vis=vis,
                      outputvis=vis+".temp_"+field,
                      field=field,
                      datacolumn="DATA")
                uvcontsub(vis=vis+".temp_"+field,
                          fitspw=fit_spw_by_field[field],
                          solint="int",
                          fitorder=0)
                list_to_concat.append(vis+".temp_"+field+".contsub")
            os.system('rm -rf '+track+'.contsub')
            concat(vis=list_to_concat,
                   concatvis=vis+".contsub")  
            os.system("rm -rf "+vis+".temp_*")
            

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# QUICK IMAGE OF THIS TRACK ONLY
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_image:

    print ""
    print "Making a preliminary image"
    print ""

    vis_list = []
    for track in track_list:
        vis_list.append(track+".split.cvel.contsub")
    if len(vis_list) == 1:
        vis_list = vis_list[0]

    os.system('rm -rf '+im_name+'.image')
    os.system('rm -rf '+im_name+'.model')
    os.system('rm -rf '+im_name+'.psf')
    os.system('rm -rf '+im_name+'.residual')
    os.system('rm -rf '+im_name+'.flux')
    clean(vis=vis_list,
          field="",
          imagename=im_name,
          mode='velocity',
          phasecenter=phasecenter,
          start=start_vel,
          width=width_vel,
          nchan=nchan_vel,
          cell=cell_size,
          imsize=im_size,
          niter=niter,
          pbcor=False,
          minpb=0.25,
          imagermode="mosaic")

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# EXPORT FITS FILE
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_export:    

    print ""
    print "Exporting a FITS file from preliminary image"
    print ""

    exportfits(
        imagename=im_name+'.image',
        fitsimage=im_name+'.fits',
        velocity = False,
        overwrite=True,
        dropstokes=True
        )

# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%
# CLEAN UP EXTRANEOUS FILES
# &%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%

if do_cleanup:

    print ""
    print "Deleting intermediate data"
    print ""
    
    pass
