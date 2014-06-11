"""
NAME

akl_21cm_autoflag

DESCRIPTION

Routines to handle autoflagging of archival VLA 21cm data sets in
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

    ### 10s quack ###

    print "... 10s at the beginning of each scan."       
    flagdata(vis=vis,mode='quack', quackinterval=10)

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


    ### Finish ###

    print "----------- autoflag_21cm ends -----------"

    # Done!
    
    return
