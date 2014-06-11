"""
NAME

akl_21cm

DESCRIPTION

Routines to handle the reduction of archival VLA 21cm data sets in
CASA.

"""
######################
### Python Imports ###
######################

# python stuff
import os
import string

# casa stuff
from tasks import *
from taskinit import *
import casac

# my casa routines
import casapy_util
    
#############################
### Import data into CASA ###
#############################

def import_21cm(
    out_root = None,
    raw_files = None,
    list_file = None,
    import_mode = 'vla',
    import_starttime = '',
    import_stoptime = '',
    import_scan = '',
    import_spw = '',
    import_timerange = '',
    import_field = '',
    log_file='import_21cm.log'
    ):
    """
    NAME

    import_21cm

    DESCRIPTION

    Import raw data (raw_files=) into a CASA ms data set
    (out_root=). Optionally carries out additional data selection
    (source=, spw=, timerange=). Saves initial flags and writes output
    of listobs to a text file.

    REQUIRED INPUTS and DEFAULTs

    out_root (None) : the stem for output. The program will write the
    ms file to out_root + '.ms' and dump the output from listobs to
    out_root+'.listobs.txt'

    raw_files (None) : list of raw files.

    -or-

    list_file (None) : file containing a list of raw files, one per
    line

    OPTIONAL INPUTS and DEFAULTs
    
    quiet (False) : suppress print statements

    import_mode ('vla') : import procedure to use. Options are 'vla'
    and 'uvfits'.

    import_starttime ('') : beginning of time range to import
    import_stoptime ('') : end of time range to import

    import_scan ('') : additional scan selection criteria
    import_spw ('') : additional spectral window selection criteria
    import_timerange ('') : additional time selection criteria
    import_field ('') : additional field selection criteria

    log_file ('import_21cm.log') : log file

    COMMENTS and FUTURE

    Could probably evolve into a fairly generic import script.

    HISTORY

    Adapted from script by Rui Xue at UIUC, who in turn adapted it
    from the NGC2403 tutorial on the CASA web pages, updated using
    casapy tricks from Josh Marvil and Miriam Krauss - Jun 2010

    Written - aleroy@nrao.edu - Sep 2010
    
    """

    ### Error check ###
    
    if (out_root == None):
        print "Need to designate an output file via [out_root=]. Returning."
        return

    if (raw_files == None) and (list_file == None):
        print "Need inputs via [raw_files=] or [list_file=]. Returning."
        return

    if (import_mode != 'vla') and (import_mode != 'uvfits'):
        print "Invalid import_mode. Select 'vla' or 'uvfits'. Returning."
        return

    ### Begin ###

    print "----------- import_21cm begins -----------"

    # reroute log output
    orig_log_file = casalog.logfile()
    casalog.setlogfile(log_file)

    ### Set up input files ###

    # define the output file
    vis = out_root + '.ms'

    # remove any previous versions
    os.system('rm -rf '+out_root+'.ms*')

    # if no file is input then read from a list of files
    if raw_files==None:
        raw_files_file=open(list_file,'r')
        lines=raw_files_file.readlines()
        raw_files_list.close()
        raw_files=[]
        for line in lines:
            line=line.strip()
            raw_files.append(line)

    ### Run import ###

    if (import_mode == 'vla'):
        print "... importvla"

        importvla(vis=vis, archivefiles=raw_files,
                  starttime=import_starttime, stoptime=import_stoptime)

    if (import_mode == 'uvfits'):
        print "... importuvfits"
        
        importuvfits(vis=vis, fitsfile=raw_files)
        
    ### Use split to apply additional selections ###
        
    if (import_scan != '' or import_spw != '' or
        import_timerange != '' or import_field != ''):

        print "... split"

        split(vis=vis, outputvis = vis+'.select',
              scan = import_scan, timerange = import_timerange,
              spw = import_spw, field = import_field)

        # replace original ms with split version
        os.system('rm -rf '+vis)
        os.system('mv '+vis+'.select '+vis)

    ### Run listobs and copy the output to a text file ###
    print "...listobs"

    casapy_util.listobs_to_file(vis,out_root+'.listobs.txt')
    
    ### Save flags with the version tag "imported" ###

    if (quiet == False):    
        print "...flagmanager"
        
    flagmanager(vis=vis, mode='save', versionname='imported',
                comment='flagging after import', merge='replace')

    ### Finish ###
    print "------------ import_21cm ends ------------"

    # set log back to its original value
    casalog.setlogfile(orig_log_file)

    return

############################
### Calibrate a data set ###
############################

def calib_21cm(
    out_root = None,
    source = None,
    spw_source ='',
    fluxcal = None,
    spw_fluxcal ='',
    fluxcal_uvrange = '',
    phasecal = None,
    spw_phasecal='',
    phasecal_uvrange = '',    
    spw_map_bp_to_flux = [],
    spw_map_bp_to_phase = [],
    ref_spw_map = [-1],
    spw_map_bp_to_source = [],
    spw_map_phase_to_source = [],
    bpcal = '',
    spw_bpcal = None,
    ref_ant='15',
    gaincurvecal=True,
    interpmode=['linear','nearest'],
    quiet=False,
    pause=False,
    reset=True
    ):
    """
    NAME

    calib_21cm

    DESCRIPTION

    Calibrate a 21cm dataset.

    REQUIRED INPUTS and DEFAULTs
    
    source (None) : name of the source

    spw_source (None) : spectral window selection for the source

    fluxcal (None) : name of the flux calibrator

    phasecal (None) : name of the phase calibrator

    bpcal (None) : name of the bandpass calibrator

    OPTIONAL INPUTS and DEFAULTs

    ref_ant ('15') : reference antenna name

    gaincurvecal (True) : apply gain curve calibration? Should be
    False if data are from pre-00

    interpmode (['linear','nearest']) : interpolation mode to use when
    applying calibration to source. First element refers to the gain
    calibration, second refers to the bandpass.
    
    quiet (False) : suppress print statements

    reset (True) : deletes previous versions of the calibration

    COMMENTS and FUTURE

    HISTORY

    Adapted from script by Rui Xue at UIUC, who in turn adapted it
    from the NGC2403 tutorial on the CASA web pages - Jun 2010

    Written - aleroy@nrao.edu - Sep 2010
    
    """

    ### Defaults and error checking ###

    if (out_root == None):
        print "Must specify root for input/output [out_root=]. Returning."
        return

    if ((source == None) or (phasecal == None) or
        (fluxcal == None) or (bpcal == None)):
        print "Must specify source, phasecal, fluxcal, and bpcal. Returning."
        return

    ### Begin ###
    
    print "----------- calib_21cm begins -----------"

    ### Define files ###

    vis = out_root+'.ms'
    
    ### Reset Calibration ###

    if (reset == True):
        if (quiet == False):
            print "... clearing previous calibration"
        
        clearcal(vis=vis)        
        os.system('rm -rf '+out_root+'.?cal'+'*')

    ### Bandpass Calibration ###
    
    if (quiet == False):
        print "... bandpass calibration"

    # a temporary per-integration phase calibration on the bpcal
        
    os.system("rm -rf "+out_root+".temp_bp_phase.gcal")
    gaincal(vis=vis, field=bpcal, spw=spw_bpcal,
            caltable=out_root+'.temp_bp_phase.gcal', gaincurve=gaincurvecal,
            calmode='p', solint='int', minsnr=2.0, refant=ref_ant)

    # run the bandpass calibration

    os.system("rm -rf "+out_root+".bpcal")
    bandpass(vis=vis, field=bpcal, spw=spw_bpcal, selectdata=False,
             caltable=out_root+'.bpcal', gaincurve=gaincurvecal,
             gaintable=out_root+'.temp_bp_phase.gcal',
             solint='inf', solnorm=True, refant=ref_ant, bandtype='B')

    ### Phase calibration ###

    print "... solving for gain calibration in each scan."

    os.system("rm -rf "+out_root+".gcal")
    gaincal(vis=vis, field=fluxcal, spw=spw_fluxcal,
            uvrange=fluxcal_uvrange, selectdata=True,
            caltable=out_root+'.gcal', append=False,
            gaintable=out_root+'.bpcal', gainfield=bpcal,
            spwmap=spw_map_bp_to_flux, interp='nearest',            
            gaincurve=gaincurvecal,
            solint='inf', minsnr=3.0, minblperant=2, refant=ref_ant)

    # loop over phase calibrators
    phasecal_list=phasecal.split(',')
    phasecal_uvrange_list=phasecal_uvrange.split(',')

    for i in range(0,len(phasecal_list)):
        gaincal(vis=vis, field=phasecal_list[i], spw=spw_phasecal,
                uvrange=phasecal_uvrange_list[i], selectdata=True,
                caltable=out_root+'.gcal', append=True,
                gaintable=out_root+'.bpcal', gainfield=bpcal,
                spwmap=spw_map_bp_to_phase, interp='nearest',
                gaincurve=gaincurvecal,
                solint='inf', minsnr=3.0, minblperant=2, refant=ref_ant)

    ### Flux calibration ###

    print "... setting flux of the primary calibrator."

    setjy(vis=vis, field=fluxcal, spw=spw_fluxcal)
    
    print "... bootstrapping this flux to the secondary calibrator."

    os.system("rm -rf "+out_root+".fcal")
    fluxscale(vis=vis, caltable=out_root+'.gcal', transfer=phasecal,
              fluxtable=out_root+'.fcal', reference=fluxcal,
              refspwmap=ref_spw_map)

    ### Apply calibration to the source ###

    print "... applying calibration tables to source."

    applycal(vis=vis, field=source, spw=spw_source,
             gaincurve=gaincurvecal,
             gaintable=[out_root+'.fcal',out_root+'.bpcal'],
             interp=interpmode, gainfield=[phasecal,bpcal],
             spwmap=[spw_map_phase_to_source, spw_map_bp_to_source])

    # Done!

    print "----------- calib_21cm ends -----------"
    
    return

##############################################
### Apply basic autoflagging to a data set ###
##############################################

def autoflag_21cm(
    out_root = None,
    edge_str = None,
    edge_chan = None,
    reset=True,
    old_version='imported'
    ):

    ### Defaults and error checking ###

    if (out_root == None):
        print "Must specify root for input/output [out_root=]. Returning."
        return

    ### Begin ###

    print "----------- autoflag_21cm begins -----------"

    ### Define files ###

    vis = out_root+'.ms'

    ### Reset Flagging  ###

    if (reset == True):
        print "... reseting flags to versionname = "+old_version        

        flagmanager(vis=vis,mode='restore',versionname=old_version)

    ### Shadowing ###

    print "... flagging shadowed data."       
    flagdata(vis=vis,mode='shadow')

    ### Autocorrelations ###

    print "... flagging autocorrelations"        
    flagautocorr(vis=vis)

    ### Edge Channels ###

    # the user gives an explicit selection string        
    if (edge_str != None):
        print "... flagging edge channels with user selection"

        flagdata(vis=vis, spw=edge_str, mode='manualflag',
                 flagbackup=False, selectdata=True)

    # the user asks for # of "edge_chan" channels to be flagged
    if (edge_chan != None):
        print "... flagging edge channels with automated selection"

        # call my "edge_channel_selection" script
        spw_string = casapy_util.edge_chan_selection(vis=vis
                                                   , edge_chan=edge_chan)
        
        flagdata(vis=vis, spw=spw_string, mode='manualflag',
                 flagbackup=False, selectdata=True)

    ### Save results ###

    flagmanager(vis=vis, mode='save', merge='replace',
                versionname='autoflagged',
                comment='flags after shadow, autocorr, edge.')

    # Done!
    
    return

#########################################
### Apply user flagging to a data set ###
#########################################

# TBD

#######################################
### Suggest flagging for a data set ###
#######################################

# TBD

###################
### Basic plots ###
###################

# TBD

#################################
### Plot derived calibrations ###
#################################

# TBD
