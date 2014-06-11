"""
NAME

akl_21cm_calib

DESCRIPTION

Routines to handle the calibration of archival VLA 21cm data sets in
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

    ###################################
    ### Defaults and error checking ###
    ###################################
    
    if (out_root == None):
        print "Must specify root for input/output [out_root=]. Returning."
        return

    if ((source == None) or (phasecal == None) or
        (fluxcal == None) or (bpcal == None)):
        print "Must specify source, phasecal, fluxcal, and bpcal. Returning."
        return
    
    #############
    ### Begin ###
    #############
    
    print "----------- calib_21cm begins -----------"

    ####################
    ### Define files ###
    ####################
    
    vis = out_root+'.ms'

    #########################
    ### Reset Calibration ###
    #########################

    if (reset == True):
        if (quiet == False):
            print "... clearing previous calibration"
        
        clearcal(vis=vis)        
        os.system('rm -rf '+out_root+'.?cal'+'*')

    #########################################
    ### First get the flux of the primary ###
    #########################################

    print "... setting flux of the primary calibrator."

    setjy(vis=vis, field=fluxcal, spw=spw_fluxcal)
    
    ############################
    ### Bandpass Calibration ###
    ############################        
    
    if (quiet == False):
        print "... bandpass calibration"

    # ... first a per-integration solution
    os.system("rm -rf "+out_root+".intphase_bpcal.gcal")
    
    gaincal(vis=vis, field=bpcal, spw=spw_bpcal,
            caltable=out_root+'.intphase_bpcal.gcal', append=False,
            gaincurve=gaincurvecal,
            calmode='p', solint='int', minsnr=2.0, refant=ref_ant)

    os.system("rm -rf "+out_root+".bpcal")
    bandpass(vis=vis, field=bpcal, spw=spw_bpcal, selectdata=False,
             caltable=out_root+'.bpcal', gaincurve=gaincurvecal,
             gaintable=out_root+'.intphase_bpcal.gcal',
             solint='inf', solnorm=True, refant=ref_ant, bandtype='B')

    #########################
    ### Phase calibration ###
    #########################
    
    print "... solving for gain calibration in each scan."

    # ... first a per-integration solution
    os.system("rm -rf "+out_root+".intphase.gcal")
    gaincal(vis=vis, field=fluxcal, spw=spw_fluxcal,
            uvrange=fluxcal_uvrange, selectdata=True,
            caltable=out_root+'.intphase.gcal', append=False,
            gaintable=out_root+'.bpcal', gainfield=bpcal,
            spwmap=spw_map_bp_to_flux, gaincurve=gaincurvecal,
            calmode='p', solint='int', minsnr=2.0, minblperant=2, refant=ref_ant)

    gaincal(vis=vis, field=phasecal, spw=spw_phasecal,
            uvrange=phasecal_uvrange, selectdata=True,
            caltable=out_root+'.intphase.gcal', append=True,
            gaintable=out_root+'.bpcal', gainfield=bpcal,
            spwmap=spw_map_bp_to_phase, gaincurve=gaincurvecal,
            calmode='p', solint='int', minsnr=2.0, minblperant=2, refant=ref_ant)

    # ... then a per-scan phase solution
    os.system("rm -rf "+out_root+".scanphase.gcal")
    gaincal(vis=vis, field=fluxcal, spw=spw_fluxcal,
            uvrange=fluxcal_uvrange, selectdata=True,
            caltable=out_root+'.scanphase.gcal', append=False,
            gaintable=out_root+'.bpcal', gainfield=bpcal,
            spwmap=spw_map_bp_to_flux, gaincurve=gaincurvecal,
            calmode='p',solint='inf', minsnr=2.0, minblperant=2, refant=ref_ant)

    gaincal(vis=vis, field=phasecal, spw=spw_phasecal,
            uvrange=phasecal_uvrange, selectdata=True,
            caltable=out_root+'.scanphase.gcal', append=True,
            gaintable=out_root+'.bpcal', gainfield=bpcal,
            spwmap=spw_map_bp_to_phase, gaincurve=gaincurvecal,
            calmode='p',solint='inf', minsnr=2.0, minblperant=2, refant=ref_ant)

    # ... then a phase-calibrated amplitude solution
    os.system("rm -rf "+out_root+".amp.gcal")
    gaincal(vis=vis, field=fluxcal, spw=spw_fluxcal,
            uvrange=fluxcal_uvrange, selectdata=True,
            caltable=out_root+'.amp.gcal', append=False,
            gaintable=[out_root+'.bpcal', out_root+'.intphase.gcal'],
            gainfield=[bpcal, fluxcal], spwmap=[spw_map_bp_to_flux, []],
            gaincurve=gaincurvecal, solint='inf', minsnr=2.0, minblperant=2,
            calmode='ap',refant=ref_ant)
    
    gaincal(vis=vis, field=phasecal, spw=spw_phasecal,
            uvrange=phasecal_uvrange, selectdata=True,
            caltable=out_root+'.amp.gcal', append=True,
            gaintable=[out_root+'.bpcal',out_root+'.intphase.gcal'],
            gainfield=[bpcal, phasecal], spwmap=[spw_map_bp_to_phase, []],
            gaincurve=gaincurvecal, solint='inf', minsnr=2.0, minblperant=2,
            calmode='ap',refant=ref_ant)

    ########################
    ### Flux calibration ###
    ########################
        
    print "... bootstrapping this flux to the secondary calibrator."

    os.system("rm -rf "+out_root+".fcal")
    fluxscale(vis=vis, caltable=out_root+'.amp.gcal', fluxtable=out_root+'.fcal',
              transfer=phasecal, reference=fluxcal, refspwmap=ref_spw_map)

    #########################
    ### Apply calibration ###
    #########################
    
    print "... applying calibration tables to source, phasecal, and fluxcal."

    # ... to the source

    applycal(vis=vis, field=source, spw=spw_source, gaincurve=gaincurvecal,
             gaintable=[out_root+'.fcal',out_root+'.scanphase.gcal',out_root+'.bpcal'],
             interp=interpmode, gainfield=[phasecal,phasecal,bpcal],
             spwmap=[spw_map_phase_to_source, spw_map_bp_to_source])

    # ... to the phase calibrator

    applycal(vis=vis, field=phasecal, spw=spw_phasecal, gaincurve=gaincurvecal,
             gaintable=[out_root+'.fcal',out_root+'.intphase.gcal',out_root+'.bpcal'],
             interp=interpmode, gainfield=[phasecal,phasecal,bpcal],
             spwmap=[[], [], spw_map_bp_to_phase])

    # ... to the flux calibrator

    applycal(vis=vis, field=fluxcal, spw=spw_fluxcal,
             gaincurve=gaincurvecal,
             gaintable=[out_root+'.fcal',out_root+'.intphase.gcal',out_root+'.bpcal'],
             interp=interpmode, gainfield=[fluxcal,fluxcal,bpcal],
             spwmap=[[], [], spw_map_bp_to_flux])

    # Done!

    print "----------- calib_21cm ends -----------"
    
    return

