"""
NAME

akl_21cm_plotgains

DESCRIPTION

Routines to make basic of calibration solutions for VLA data.

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
    
#####################################
### plot the bandpass calibration ###
#####################################

def plotgains_21cm(
    bptable='',
    phasetable='',
    amptable='',
    plot_root = '',
    plotformat = 'png',
    spawn_xv = False,
    pause=False
    ):

    #################################
    ### Plot bandpass calibration ###
    #################################

    plotcal(caltable=bptable, iteration='antenna', subplot=321,
            xaxis='freq', yaxis='phase', plotrange=[0,0,-180,180],
            figfile=plot_root+'_bpphase.png')

    if (pause == True):
        dummy = raw_input("Hit <Enter> to proceed with script.")

    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')
        
    plotcal(caltable=bptable, iteration='antenna', subplot=321,
            xaxis='freq', yaxis='amp', figfile=plot_root+'_bpamp.png')

    if (pause == True):
        dummy = raw_input("Hit <Enter> to proceed with script.")

    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')

    #############################
    ### Plot scan-based phase ###
    #############################

    plotcal(caltable=phasetable, iteration='antenna', subplot=321,
            xaxis='time', yaxis='phase', plotrange=[0,0,-180,180],
            figfile=plot_root+'_phase.png')

    if (pause == True):
        dummy = raw_input("Hit <Enter> to proceed with script.")

    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')

    ###########################
    ### Plot scan-based amp ###
    ###########################

    plotcal(caltable=amptable, iteration='antenna', subplot=211,
        xaxis='time', yaxis='amp', figfile=plot_root+'_amp.png')

    if (pause == True):
        dummy = raw_input("Hit <Enter> to proceed with script.")

    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')

    ### Finish ###

    print "----------- plotgains_21cm ends -----------"

    # Done!
    
    return
