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
    
#########################################
### Make plots of phase and amplitude ###
#########################################

def plotphaseandamp_21cm(
    out_root = None,
    field = None,
    spw ='',
    plot_dir = '',
    tag = 'beforecal',
    column = 'data',
    plotformat = 'png',
    spawn_xv = False
    ):

    ### Defaults and error checking ###

    if (out_root == None):
        print "Must specify root for input/output [out_root=]. Returning."
        return

    ### Begin ###

    print "----------- plotphaseandamp_21cm begins -----------"

    ### Define files ###

    vis = out_root+'.ms'

    timebin = 'all'
        
    ### Plot amplitude vs. time    
    fig_file = plot_dir + field+'_amp_vs_time_'+tag+'.'+plotformat
    
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='time', yaxis='amp', averagemode='vector',
           timebin=timebin, width='all', datacolumn=column,
           plotsymbol='.', markersize=0.1, fontsize=6.0,
           figfile=fig_file, interactive = False)
    
    if (spawn_xv == True):                
        os.system('xv '+fig_file+' &')            
        
    ### Plot phase vs time ###

    fig_file = plot_dir + field+'_phase_vs_time_'+tag+'.'+plotformat
    
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='time', yaxis='phase', averagemode='vector',
           timebin=timebin, width='all', datacolumn=column,
           plotsymbol='.', markersize=0.1, fontsize=6.0,
           figfile=fig_file, interactive = False)
    
    if (spawn_xv == True):                
        os.system('xv '+fig_file+' &')
        
    ### Plot amp vs. uv-distance ###

    fig_file = plot_dir + field+'_amp_vs_uvdist_'+tag+'.'+plotformat
        
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='uvdist', yaxis='amp', averagemode='vector',
           timebin=timebin, width='all', datacolumn=column,
           plotsymbol='.', markersize=0.1, fontsize=6.0,
           figfile=fig_file, interactive = False)
    
    if (spawn_xv == True):                
        os.system('xv '+fig_file+' &')
        
    ### Plot phase vs. uv-distance ###

    fig_file = plot_dir + field+'_phase_vs_uvdist_'+tag+'.'+plotformat
    
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='uvdist', yaxis='phase', averagemode='vector',
           timebin=timebin, width='all', datacolumn=column,
           plotsymbol='.', markersize=0.1, fontsize=6.0,
           figfile=fig_file, interactive = False)
        
    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')
        
    ### Plot phase vs. channel ###

    fig_file = plot_dir + field+'_phase_vs_chan_'+tag+'.'+plotformat
    
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='chan', yaxis='phase', averagemode='vector',
           timebin=timebin, width='1', datacolumn=column,
           plotsymbol='.', markersize=0.1, fontsize=6.0,
           figfile=fig_file, interactive = False)
    
    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')
        
    ### Plot amp vs. channel ###

    fig_file = plot_dir + field+'_amp_vs_chan_'+tag+'.'+plotformat
    
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='chan', yaxis='amp', averagemode='vector',
           timebin=timebin, width='1', datacolumn=column,
           plotsymbol='.', markersize=0.1, fontsize=6.0,
           figfile=fig_file, interactive = False)
    
    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')
        
    ### Plot an integrated spectrum ###

    fig_file = plot_dir + field+'_intspec_'+tag+'.'+plotformat
    
    plotxy(vis=vis, spw=spw, field=field,
           xaxis='freq', yaxis='amp', averagemode='vector',
           timebin='all', width='1', crossscans=True,
           crossbls=True, datacolumn=column,
           plotsymbol='o', markersize=5.0, fontsize=6.0,
           figfile=fig_file, interactive = False)
    
    if (spawn_xv == True):
        os.system('xv '+fig_file+' &')

    ### Finish ###

    print "----------- plotphaseandamp_21cm ends -----------"

    # Done!
    
    return
