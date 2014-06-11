"""
NAME

akl_21cm_plotcalib

DESCRIPTION

Routines to make calibration plots for archival VLA 21cm data sets in CASA.

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

def plotcalib_21cm(
    out_root = None,
    source = None,
    spw_source ='',
    fluxcal = '',
    spw_fluxcal ='',
    phasecal = '',
    spw_phasecal='',
    bpcal = '',
    spw_bpcal ='',
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


### Rui's plot of the bandpass solution


    bpcal_table = ''

    
    print "... plot bandpass solutions for each antenna"

    plotcal(vis=vis, caltable=bpcal_table)
    
    default('plotcal')
    vis = msfile
    caltable = prefix+'.bcal'
    field = passcal
    selectplot=True
    plotsymbol='.'
    markersize=0.1
    fontsize=6.0
        
    merge_eps='gs -sDEVICE=pdfwrite -sOutputFile='+prefix+'.plotcal.bandpass.pdf'
    merge_eps=merge_eps+' -dNOPAUSE -dBATCH'
    
    for i in range(0,num_ant-1):
        antenna=str(i)
        for j in range(0,len(spw_bpcal)):
            spw=spw_bpcal[j]
            plotrange = [-1, -1, 0.6, 1.4]
            

            subplot = 2*100+len(spwid_passcal)*10+1+j
            xaxis = 'chan'
            yaxis = 'amp'
            figfile=prefix+'.plotcal.bandpass.ant'+str(i)+'.pdf'
            plotcal()
            subtitle='Bandpass Solution: Antenna '+str(i)+' SpwID '+spwid_passcal[j]
            pl.title(subtitle,fontsize=6)        
           
            spw=spwid_passcal[j]
            plotrange = [-1, -1, -45, 45]
            subplot = 2*100+len(spwid_passcal)*10+len(spwid_passcal)+j+1
            xaxis=  'chan'
            yaxis = 'phase'
            figfile=prefix+'.plotcal.bandpass.ant'+str(i)+'.pdf'
            title='Passband Solution, Antenna '+str(i)+ 'SpwID '+spwid_passcal[j]
            plotcal()
        
        merge_eps=merge_eps+' '+prefix+'.plotcal.bandpass.ant'+str(i)+'.pdf'
    
    os.system(merge_eps)
    os.system('rm '+prefix+'.plotcal.bandpass.ant*.pdf')
    print ""

if  noplot==False:
    print ""
    print "--plotcal--"
    print ""
    print "Plot bandpass solutions for all antennae"
    
    default('plotcal')
    vis = msfile
    caltable = prefix+'.bcal'
    field = passcal
    selectplot=True
    plotsymbol='.'
    markersize=0.1
    fontsize=6.0
    if nogui:
        showgui = False      
    for j in range(0,len(spwid_passcal)):
        spw=spwid_passcal[j]
        plotrange = [-1, -1, 0.6, 1.4]
        subplot = 2*100+len(spwid_passcal)*10+1+j
        xaxis = 'chan'
        yaxis = 'amp'
        figfile=prefix+'.plotcal.allbandpass.'+plotformat
        plotcal()
        subtitle='Bandpass Solution'
        pl.title(subtitle,fontsize=6)       
        spw=spwid_passcal[j]
        plotrange = [-1, -1, -90, 90]
        subplot = 2*100+len(spwid_passcal)*10+len(spwid_passcal)+j+1
        xaxis = 'chan'
        yaxis = 'phase'
        figfile=prefix+'.plotcal.allbandpass.'+plotformat
        title='Passband Solution'
        plotcal()
    print ""


    ### Define files ###

    vis = out_root+'.ms'

    fields = []
    spw_strs = []

    if (source != ''):
        fields += [source]
        spw_strs += [spw_source]

    if (phasecal != ''):
        fields += [phasecal]
        spw_strs += [spw_phasecal]

    if (fluxcal != ''):
        fields += [fluxcal]
        spw_strs += [spw_fluxcal]

    for i in range(0,len(fields)):

        field = fields[i]
        spw_str = spw_strs[i]

        if (field == fluxcal):
            timebin = '0'
        else:
            timebin = 'all'
        
    ### Plot amplitude vs. time

        fig_file = plot_dir + field+'_amp_vs_time_'+tag+'.'+plotformat
        
        plotxy(vis=vis, spw=spw_str, field=field,
               xaxis='time', yaxis='amp', averagemode='vector',
               timebin=timebin, width='all', datacolumn=column,
               plotsymbol='.', markersize=0.1, fontsize=6.0,
               figfile=fig_file, interactive = False)

        if (spawn_xv == True):                
            os.system('xv '+fig_file+' &')            
        
    ### Plot phase vs time ###

        fig_file = plot_dir + field+'_phase_vs_time_'+tag+'.'+plotformat
        
        plotxy(vis=vis, spw=spw_str, field=field,
               xaxis='time', yaxis='phase', averagemode='vector',
               timebin=timebin, width='all', datacolumn=column,
               plotsymbol='.', markersize=0.1, fontsize=6.0,
               figfile=fig_file, interactive = False)

        if (spawn_xv == True):                
            os.system('xv '+fig_file+' &')

    ### Plot amp vs. uv-distance ###

        fig_file = plot_dir + field+'_amp_vs_uvdist_'+tag+'.'+plotformat
                
        plotxy(vis=vis, spw=spw_str, field=field,
               xaxis='uvdist', yaxis='amp', averagemode='vector',
               timebin=timebin, width='all', datacolumn=column,
               plotsymbol='.', markersize=0.1, fontsize=6.0,
               figfile=fig_file, interactive = False)

        if (spawn_xv == True):                
            os.system('xv '+fig_file+' &')
            
    ### Plot phase vs. uv-distance ###

        fig_file = plot_dir + field+'_phase_vs_uvdist_'+tag+'.'+plotformat
                
        plotxy(vis=vis, spw=spw_str, field=field,
               xaxis='uvdist', yaxis='phase', averagemode='vector',
               timebin=timebin, width='all', datacolumn=column,
               plotsymbol='.', markersize=0.1, fontsize=6.0,
               figfile=fig_file, interactive = False)
        
        if (spawn_xv == True):

#----------------------------------------------------------------------------------------
#   Plot antenna gains
#----------------------------------------------------------------------------------------
if  noplotcal!=True and noplot==False:

    print ""
    print "--plotcal--"
    print ""
    print "Plot the amplitude/phase/SNR of flux scaled gain solutions for each antenna"

    default('plotcal')
    caltable= prefix + '.fcal'
    xaxis='time'
    selectplot=True
    
    if nogui:
        showgui = False

    merge_eps='gs -sDEVICE=pdfwrite -sOutputFile='+prefix+'.plotcal.gscaled.pdf'
    merge_eps=merge_eps+' -dNOPAUSE -dBATCH'
    
    for i in range(0,num_ant-1):
    
        antenna=str(i)
        field=phasecal+','+fluxcal
        yaxis='amp'
        subplot=311
        figfile=prefix+'.plotcal.gscaled.ant'+str(i)+'.pdf'
        plotsymbol='.'
        markersize=0.1
        fontsize=6.0
        title='Antenna '+str(i)
        plotcal()
        subtitle='Gain Solution: Antenna '+str(i)+' SpwID '+spwid_passcal[j]
        pl.title(subtitle,fontsize=6)
    
        yaxis='phase'
        subplot=312
        figfile=prefix+'.plotcal.gscaled.ant'+str(i)+'.pdf'
        plotsymbol='.'
        markersize=0.1
        fontsize=6.0
        title='Antenna '+str(i)
        plotcal()
    
        yaxis='snr'
        subplot=313
        figfile=prefix+'.plotcal.gscaled.ant'+str(i)+'.pdf'
        plotsymbol='.'
        markersize=0.1
        fontsize=6.0
        title='Antenna '+str(i)
        plotcal()
        
        merge_eps=merge_eps+' '+prefix+'.plotcal.gscaled.ant'+str(i)+'.pdf'
    
    os.system(merge_eps)
    os.system('rm '+prefix+'.plotcal.gscaled.ant*.pdf')
    print ""

if  noplot==False:

    print ""
    print "--plotcal--"
    print ""
    print "Plot the amplitude/phase/SNR of flux scaled gain solutions for all antennae"

    default('plotcal')
    caltable= prefix + '.fcal'
    xaxis='time'
    selectplot=True
    if nogui:
        showgui = False  
    field=phasecal+','+fluxcal
    yaxis='amp'
    subplot=311
    figfile=prefix+'.plotcal.allgscaled.'+plotformat
    plotsymbol='.'
    markersize=0.1
    fontsize=6.0
    plotcal()
    subtitle='Gain Solution'
    pl.title(subtitle,fontsize=6)

    yaxis='phase'
    subplot=312
    figfile=prefix+'.plotcal.allgscaled.'+plotformat
    plotsymbol='.'
    markersize=0.1
    fontsize=6.0
    plotcal()
    yaxis='snr'
    subplot=313
    figfile=prefix+'.plotcal.allgscaled.'+plotformat
    plotsymbol='.'
    markersize=0.1
    fontsize=6.0
    plotcal()
    print ""



    ### Finish ###

    print "----------- plotcalib_21cm ends -----------"

    # Done!
    
    return
