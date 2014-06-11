"""
NAME

akl_21cm_basicplots

DESCRIPTION

Routines to make basic plots for archival VLA 21cm data sets in CASA.

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

def basicplots_21cm(
    out_root = None,
    plot_dir = '',
    source = None,
    plotformat = 'png',
    spawn_xv = False,    
    ):

    ### Defaults and error checking ###

    if (out_root == None):
        print "Must specify root for input/output [out_root=]. Returning."
        return

    ### Begin ###

    print "----------- basicplots_21cm begins -----------"

    ### Define files ###

    vis = out_root+'.ms'

    ### Plot UV coverage  ###
    fig_file = plot_dir+source+'.uvcoverage.'+plotformat
    
    plotxy(vis=vis,field=source,xaxis='u',yaxis='v',
           figfile=fig_file, interactive = False,
           plotsymbol='.',markersize=0.1, fontsize=6.0,
           averagemode='vector', timebin='60')

    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')

    ### Plot antenna positions ###
    fig_file = plot_dir+'antpos.'+plotformat
    plotants(vis=vis,figfile=fig_file)

    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')

    ### Finish ###

    print "----------- basicplots_21cm ends -----------"

    # Done!
    
    return
