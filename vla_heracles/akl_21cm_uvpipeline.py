"""
NAME

akl_21cm_uvpipeline

DESCRIPTION

Import, flag, calibrate, and continuum-subtract VLA 21cm data

"""
######################
### Python Imports ###
######################

# python stuff
import os
import string
import numpy

# casa stuff
from tasks import *
from taskinit import *
import casac

# my casa routines
import casapy_util
    
#######################
### The UV Pipeline ###
#######################

def uvpipeline(
    out_root = None,
    log_file='pipeline.log',
    # STEPS TO PERFORM
    do_import = True,
    do_flag = True,
    do_calib = True,
    do_split = True,
    do_hanning = False,   
    do_uvsub = True,
    # IMPORT INFORMATION
    raw_files = None,
    import_mode = 'vla',
    import_starttime = '',
    import_stoptime = '',
    import_scan = '',
    import_spw = '',
    import_timerange = '',
    import_field = '',
    # FLAGGING INFORMATION
    reset_flags = True,
    do_autoflag = True,
    edge_chan = 7,
    user_flags = None,
    # CALIBRATION INFORMATION
    reset_cal = True,
    # ... source ID:
    source = '',
    phasecal = '',
    fluxcal = '',
    bpcal = '',
    model_fluxcal = "",
    # ... calibration methodology:
    ref_ant = None,
    gaincurvecal = False,
    interpmode = ['linear','linear','nearest'],
    # ... spectral window mapping:
    spw_map_bpcal_cal = [],
    spw_map_bpcal_source =[],
    spw_map_cal_source =[],
    fluxscale_refspwmap = [-1],
    # ... set the flux of the phasecal by hand:
    setjy_phasecal = False,
    setjy_field = "",
    setjy_spw = "",
    setjy_fluxdensity = "",
    # SPLIT INFORMATION
    do_cvel = False,
    # HANNING SMOOTHING INFORMATION
    n_han = 1,
    # UV SUBTRACTION INFORMATION
    uvsub_order = 1,
    uvsub_spw = '',
    uvsub_solint = 'int',
    uvsub_uvcontsub2 = True,
    # SET INTERACTION LEVEL
    interactive = False,
    reset_log = True,
    show = True
    ):
    """
    """

    #############################################
    ### Step 0: CHECK INPUTS AND SET DEFAULTS ###
    #############################################

    if (out_root == None):
        print "Need to designate an output file via [out_root=]. Returning."
        return
    
    # reroute log output
    orig_log_file = casalog.logfile()
    if (reset_log == True):
        os.system('rm -rf '+log_file)
    casalog.setlogfile(log_file)

    # define the output file
    vis = out_root + '.ms'

    ######################
    ### Step 1: IMPORT ###
    ######################
    
    # Import data from the supplied list then split out the desired
    # subset of data and run listobs.

    if do_import:
        print "---------------"
        print "STEP #1: IMPORT"
        print "---------------"

        ### Check inputs ###
        if (raw_files == None):
            print "Need inputs via [raw_files=] . Returning."
            casalog.setlogfile(orig_log_file)
            return
        
        if (import_mode != 'vla') and (import_mode != 'uvfits'):
            print "Invalid import_mode. Select 'vla' or 'uvfits'. Returning."
            casalog.setlogfile(orig_log_file)
            return

        ### Remove previous versions ###
        os.system('rm -rf '+out_root+'.ms*')

        ### Run import task ###
        if (import_mode == 'vla'):
            print "... importvla"
            importvla(vis=vis, archivefiles=raw_files,
                      starttime=import_starttime, stoptime=import_stoptime)

        if (import_mode == 'uvfits'):
            print "... importuvfits"
            importuvfits(vis=vis, fitsfile=raw_files)

        ### Use SPLIT to apply additional selections ###            
        if (import_scan != '' or import_spw != '' or
            import_timerange != '' or import_field != ''):
            print "... split"

            split(vis=vis, outputvis = vis+'.select',
                  scan = import_scan, timerange = import_timerange,
                  spw = import_spw, field = import_field,
                  datacolumn='data')

            ### Replace original ms with split version
            os.system('rm -rf '+vis)
            os.system('mv '+vis+'.select '+vis)

        ### Run LISTOBS, directing output to a text file ###
        print "...listobs"
        os.system("rm -rf "+out_root+".listobs.txt")
        casapy_util.listobs_to_file(vis,out_root+'.listobs.txt')
        os.system("cat "+out_root+".listobs.txt")

        ### Save flags with the version tag "imported" ###
        print "...flagmanager"        
        flagmanager(vis=vis, mode='save', versionname='imported',
                    comment='flagging after import', merge='replace')

    ########################
    ### Step 2: FLAGGING ###
    ########################

    # Flag bad data. This has two parts: an automated pruning of
    # certain subsets of the data that are likely to be bad and
    # applying a list of flags supplied by the user.

    if do_flag:
        print "-----------------"
        print "STEP #2: FLAGGING"
        print "-----------------"

        ### By default revert to the imported version ###
        old_version='imported'

        ### Reset flags to the old version ###
        if (reset_flags == True):            
            #print "... reseting flags to versionname = "+old_version
            print "... reseting flags"
            flagdata(vis=vis,mode="manualflag",unflag=True,flagbackup=False)
            #flagmanager(vis=vis,mode='restore',versionname=old_version)

        ### Automatically flag certain subsets of the data ###
        if do_autoflag:
            
            ### 30s quack ###
            print "... 30s at the beginning of each scan."       
            flagdata(vis=vis,mode='quack', quackinterval=30)
        
            ### Shadowing ###
            print "... flagging shadowed data."       
            flagdata(vis=vis,mode='shadow')

            ### Autocorrelations ###
            print "... flagging autocorrelations"        
            flagautocorr(vis=vis)
            
            ### Edge channels ###
            if (edge_chan != None):
                print "... flagging edge channels with automated selection"
                spw_string = casapy_util.edge_chan_selection(vis=vis, edge_chan=edge_chan)
                flagdata(vis=vis, spw=spw_string, mode='manualflag',
                         flagbackup=False, selectdata=True)

        ### Apply user-specified flagging ###
        if (user_flags != None):

            ### Initialize lists of flagging selections
            antenna = []
            spw = []
            correlation = []
            field = []
            uvrange = []
            timerange = []
            scan = []

            ### USER_FLAGS is expected to be a list of
            ### dictionaries. Each dictionary refers to one flagging
            ### command with the keys indicating the selections for
            ### that run. Loop over these dictionaries and fill in the
            ### lists with the appropriate selections, setting them to
            ### be blank ("") if not specified. This lets the whole
            ### set of flags be applied in a single flagdata call.
            
            for flag in user_flags:
                if flag.has_key("antenna"):
                    antenna.append(flag["antenna"])
                else:
                    antenna.append("")

                if flag.has_key("spw"):
                    spw.append(flag["spw"])
                else:
                    spw.append("")

                if flag.has_key("correlation"):
                    correlation.append(flag["correlation"])
                else:
                    correlation.append("")

                if flag.has_key("field"):
                    field.append(flag["field"])
                else:
                    field.append("")

                if flag.has_key("uvrange"):
                    uvrange.append(flag["uvrange"])
                else:
                    uvrange.append("")

                if flag.has_key("timerange"):
                    timerange.append(flag["timerange"])
                else:
                    timerange.append("")

                if flag.has_key("scan"):
                    scan.append(flag["scan"])
                else:
                    scan.append("")

            ### Call FLAGDATA ###
            if (len(user_flags) > 0):
                print "... flagdata for user flags."
                flagdata(vis=vis,
                         mode='manualflag',
                         selectdata=True,
                         flagbackup=False,
                         antenna=antenna,
                         spw=spw,
                         correlation=correlation,
                         field=field,
                         uvrange=uvrange,
                         timerange=timerange,
                         scan=scan)
            
    #########################
    ### Step 3: CALIBRATE ###
    #########################

    # Calibrate the data. This has three parts: flux (amplitude)
    # calibration, phase calibration, and bandpass
    # calibration. Several supporting calibrations are also carried
    # out. Right now there is not sophisticated spectral window
    # handling but this may need to improve as we try out more data.

    if do_calib:

        ### Error checking ###
        
        if ((source == None) or (phasecal == None) or
            (fluxcal == None) or (bpcal == None)):
            print "Specify source, phasecal, fluxcal, and bpcal to calibrate. Returning."
            casalog.setlogfile(orig_log_file)
            return

        ### Suggest refant if none supplied ###
        if (ref_ant == None):

            # Will return the antenna closest to the mean center of
            # the array but still above MIN_SEP and with less than the
            # 1.0+FLAG_THRESH times the mean amount of flagging.

            ref_ant = casapy_util.suggest_refant(vis = out_root+'.ms',
                                                 min_sep = 35.0,
                                                 flag_thresh = 0.0)
            

        print "--------------------"
        print "STEP #3: CALIBRATION"
        print "--------------------"

        ### Reset calibration ###
        if (reset_cal == True):
            print "... clearcal"
            clearcal(vis=vis)        
            os.system('rm -rf '+out_root+'.?cal'+'*')

        ### Check for duplicate cals
        if (phasecal == fluxcal):
            cals = fluxcal
        else:
            cals = fluxcal+','+phasecal

        ### Set the flux scale
        print "... setjy"
        setjy(vis=vis, field=fluxcal, modimage=model_fluxcal)

        ### ... optionally set the flux scale by hand
        if setjy_phasecal:
            setjy(vis=vis, field=setjy_field, spw=setjy_spw, fluxdensity=setjy_fluxdensity)
        ### Do a short-timescale phase selfcal on the bandpass calibrator
        print "... a short phase self-cal on the bandpass calibrator."
        os.system("rm -rf "+out_root+".intphase_bpcal.gcal")
        gaincal(vis=vis, field=bpcal, caltable=out_root+'.intphase_bpcal.gcal',
                append=False, gaincurve=gaincurvecal, calmode='p',
                solint='int', minsnr=2.0, refant=ref_ant)

        ### Do the bandpass calibration
        print "... bandpass calibration"
        os.system("rm -rf "+out_root+".bpcal")
        bandpass(vis=vis, field=bpcal, selectdata=False,
                 caltable=out_root+'.bpcal', gaincurve=gaincurvecal,
                 gaintable=out_root+'.intphase_bpcal.gcal',
                 solint='inf', solnorm=True, refant=ref_ant, bandtype='B')

        ### Do a per-scan phase solution
        print "... a phase gaincal (per scan)"
        os.system("rm -rf "+out_root+".scanphase.gcal")
        gaincal(vis=vis, field=cals, selectdata=True,
                caltable=out_root+'.scanphase.gcal', append=False,
                gaintable=out_root+'.bpcal', gainfield=bpcal,
                gaincurve=gaincurvecal, calmode='p',solint='inf',
                minsnr=2.0, minblperant=2, refant=ref_ant,
                spwmap = spw_map_bpcal_cal)

        ### Do short-timescale phase selfcal on the phase & flux calibrators
        print "... a phase gaincal (per integration)"
        os.system("rm -rf "+out_root+".intphase.gcal")
        gaincal(vis=vis, field=cals, selectdata=True,
                caltable=out_root+'.intphase.gcal', append=False,
                gaintable=out_root+'.bpcal', gainfield=bpcal,
                gaincurve=gaincurvecal, calmode='p', solint='int',
                minsnr=2.0, minblperant=2, refant=ref_ant,
                spwmap = spw_map_bpcal_cal)

        ### Do the amplitude calibration
        print "... an amplitude gaincal (per scan)"
        os.system("rm -rf "+out_root+".amp.gcal")
        gaincal(vis=vis, field=cals, selectdata=True,
                caltable=out_root+'.amp.gcal', append=False,
                gaintable=[out_root+'.bpcal', out_root+'.intphase.gcal'],
                gainfield=[bpcal, fluxcal+','+phasecal], 
                gaincurve=gaincurvecal, solint='inf', minsnr=2.0, minblperant=2,
                calmode='a',refant=ref_ant,
                spwmap = [spw_map_bpcal_cal,[]])

        ### Apply the flux scale to the amplitude calibration
        print "... fluxscale on the amplitude gaincal"        
        os.system("rm -rf "+out_root+".fcal")
        if (setjy_phasecal == False) and (phasecal != fluxcal):
            fluxscale(vis=vis, caltable=out_root+'.amp.gcal', fluxtable=out_root+'.fcal',
                      transfer=phasecal, reference=fluxcal, refspwmap=fluxscale_refspwmap)
        else:
            os.system("cp -r "+out_root+".amp.gcal "+out_root+".fcal")

        ### Apply calibrations to ...

        # ... the source
        print "... applycal to source"
        applycal(vis=vis, field=source, gaincurve=gaincurvecal,
                 gaintable=[out_root+'.fcal',out_root+'.scanphase.gcal',out_root+'.bpcal'],
                 interp=interpmode, gainfield=[phasecal,phasecal,bpcal],
                 spwmap=[spw_map_cal_source,spw_map_cal_source,
                         spw_map_bpcal_source])
        
        # ... the phase calibrator
        print "... applycal to phase calibrator"
        applycal(vis=vis, field=phasecal, gaincurve=gaincurvecal,
                 gaintable=[out_root+'.fcal',out_root+'.scanphase.gcal',out_root+'.bpcal'],
                 interp=interpmode, gainfield=[phasecal,phasecal,bpcal],                 
                 spwmap=[[],[],spw_map_bpcal_cal])
        
        # ... the flux calibrator
        print "... applycal to flux calibrator"
        applycal(vis=vis, field=fluxcal, gaincurve=gaincurvecal,
                 gaintable=[out_root+'.fcal',out_root+'.intphase.gcal',out_root+'.bpcal'],
                 interp=interpmode, gainfield=[fluxcal,fluxcal,bpcal],               
                 spwmap=[[],[],spw_map_bpcal_cal])

        ### Plot calibration if desired ###
        if show:
            # amp vs. channel
            plotcal(caltable=out_root+'.bpcal', xaxis='chan', yaxis='phase',
                   plotrange=[0,0,-180,180], iteration='antenna', subplot=331)
            dummy = raw_input("Phase. vs. chan. Hit <Enter> to continue ...")

            # amp vs. channel
            plotcal(caltable=out_root+'.bpcal', xaxis='chan', yaxis='amp',
                   iteration='antenna', subplot=331)
            dummy = raw_input("Amp. vs. chan. Hit <Enter> to continue ...")

            # phase vs. time
            plotcal(caltable=out_root+'.scanphase.gcal', xaxis='time', yaxis='phase',
                   plotrange=[0,0,-180,180], iteration='antenna', subplot=331)
            dummy = raw_input("Phase vs. time. Hit <Enter> to continue ...")

            # amp vs. time
            plotcal(caltable=out_root+'.fcal', xaxis='time', yaxis='amp',
                   iteration='antenna', subplot=331)
            dummy = raw_input("Amp. vs. time. Hit <Enter> to continue ...")

    #####################
    ### Step 4: SPLIT ###
    #####################

    # Separate the source from the rest of the data, appropriate for
    # later imaging and concatenation into a single large uv
    # file. Optionally regrid the source after splitting to have a
    # single spectral window. This is useful when a source with a
    # large line width has been observed with successive spectral
    # windows.

    if do_split:

        if (source == None):
            print "Specify source to splitcalibrate. Returning."
            casalog.setlogfile(orig_log_file)
            return

        print "-------------------------"
        print "STEP #4: SPLIT OUT SOURCE"
        print "-------------------------"

        ### Split the source out of the main data set
        print "... split on main source"
        os.system('rm -rf '+out_root+'.split.ms')
        split(vis=out_root+'.ms',
              outputvis=out_root+'.split.ms',
              field=source,
              datacolumn='corrected')

        ### Regrid the source to have a single spectral window
        if do_cvel:
            print "... cvel on main source"
            os.system('rm -rf '+out_root+'.split.ms.cvel')
            cvel(vis=out_root+'.split.ms',
                 outputvis=out_root+'.split.ms.cvel', mode='channel',
                 interpolation='cubic')
            os.system('rm -rf '+out_root+'.split.ms')
            os.system('mv '+out_root+'.split.ms.cvel '+out_root+'.split.ms')

    ##############################
    ### Step 5: HANNING SMOOTH ###
    ##############################

    # Apply hanning smoothing to the final data set. CLEAN only
    # interpolates when doing a spectral regridding, so this is useful
    # if you plan to bin to a lower velocity resolution at a later
    # stage.

    if do_split and do_hanning:

        print "--------------------------"
        print "STEP #5: HANNING SMOOTHING"
        print "--------------------------"

        ### Apply hanning smoothing ###
        print "... hanning smooth on main source "+str(n_han)+" times"
        print "... (N.B. only done when splitting)"

        for i in range(n_han):
            os.system('rm -rf '+out_root+'.hanning.ms')
            hanningsmooth(vis=out_root+'.split.ms', datacolumn='all',
                          outputvis=out_root+'.hanning.ms')
            os.system('rm -rf '+out_root+'.split.ms')
            os.system('mv '+out_root+'.hanning.ms '+out_root+'.split.ms')

    ##################################
    ### Step 6: CONTINUUM SUBTRACT ###
    ##################################

    # Continuum subtract the calibrated, split uv data. Carries out a
    # fit to the specified channels, subtracts, and leaves the data in
    # the CORRECTED column. Default is to carry out a per-scan uv
    # subtraction to get the SNR up.

    if do_uvsub:

        ### Error checking ###
        
        print "------------------------------"
        print "STEP #6: CONTINUUM SUBTRACTION"
        print "------------------------------"

        print "WARNING! Do NOT run this step repeatedly. You NEED to re-split."

        ### Continuum subtraction ###
        if (uvsub_uvcontsub2 == True):        
            print "... uvcontsub2 on main source. Note that this FORCES order zero."
            os.system('rm -rf '+out_root+'.split.ms.contsub')
            clearcal(vis=out_root+'.split.ms')
            uvcontsub2(vis=out_root+'.split.ms', fitspw=uvsub_spw, solint=uvsub_solint)
            os.system('rm -rf '+out_root+'.split.ms')
            os.system('mv '+out_root+'.split.ms.contsub '+out_root+'.split.ms')
        else:
            print "... uvcontsub on main source. Be careful of history!"
            uvcontsub(vis=out_root+'.split.ms', fitorder=uvsub_order,
                      fitspw=uvsub_spw, solint=uvsub_solint)

        ### Plot Spectrum Before and After Continuum Subtraction ###
        if show:
            plotms(vis=out_root+'.split.ms', xaxis='chan',
                   yaxis='amp', ydatacolumn='data', averagedata=True,
                   avgtime='1e9',avgscan=True,avgfield=True,avgbaseline=True)
            dummy = raw_input('Data before subtraction. Hit <Enter> to see subtraction.')
            plotms(vis=out_root+'.split.ms', xaxis='chan',
                   yaxis='amp', ydatacolumn='corrected', averagedata=True,
                   avgtime='1e9',avgscan=True,avgfield=True,avgbaseline=True)            

    ### Wrap up by resetting log file
    casalog.setlogfile(orig_log_file)        
    return
