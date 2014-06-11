"""
NAME

akl_21cm_impipeline

DESCRIPTION

Concatenate, invert, clean, and export VLA 21cm data.

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
    
############################
### The Imaging Pipeline ###
############################

def impipeline(
    out_root = None,
    log_file='pipeline.log',
    # STEPS TO PERFORM
    do_concat = True,
    do_image = True,
    do_clean = True,
    do_export = True,
    # CONCATENATE INFORMATION
    ms_files = None,
    # IMAGING INFORMATION
    cell = "2arcsec",
    imsize = [1024,1024],
    restfreq = '1420405752.0Hz',
    weighting = 'briggs',
    robust = 0.0,
    pbcor = False,
    # ... LINE SETUP
    noline = False,
    nchan = None,
    v0 = None,
    deltav = None,
    # CLEAN INFORMATION
    threshold = "0.0mJy/beam",
    imagermode = "",
    multiscale = [],
    clean_mask_fits = "",
    clean_mask = "",
    niter = 5000,
    # EXPORT INFORMATION
    out_fits_root = None,
    # SET INTERACTION LEVEL
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

    ###########################
    ### Step 1: CONCATENATE ###
    ###########################
    
    # Concate a list of calibrated uv-files into a single data set.

    if do_concat:
        print "---------------"
        print "STEP #1: CONCAT"
        print "---------------"

        ### Check inputs ###
        if (ms_files == None):
            print "Need inputs via [ms_files=] . Returning."
            casalog.setlogfile(orig_log_file)
            return
        
        ### Remove previous versions ###
        os.system('rm -rf '+out_root+'.ms*')
        os.system('rm -rf '+ out_root + '.listobs.txt')
        
        ### Run concat ###
        concat(vis=ms_files, concatvis=out_root+'.ms', dirtol='1.arcsec')

        ## Run listobs afterwards ###
        casapy_util.listobs_to_file(out_root+'.ms', log_file=out_root+'.listobs.txt')
        os.system('cat '+ out_root + '.listobs.txt')

    #######################
    ### Step 2: IMAGING ###
    #######################

    # Image the concatenated data, resulting in a dirty cube that we
    # can look at before cleaning and use to estimate the threshold used to clean

    if do_image:
        print "----------------"
        print "STEP #2: IMAGING"
        print "----------------"

        ### Remove previous versions ###
        os.system('rm -rf '+out_root+'.dirty*')

        ### Invert but don't clean ###
        clean(vis=out_root+'.ms', imagename=out_root+'.dirty',
              restfreq=restfreq, mode='velocity',
              width = deltav, nchan = nchan, start=v0,
              cell=cell, imsize=imsize, weighting=weighting,
              robust=robust, niter=0, pbcor=pbcor,
              interpolation='cubic')

    #####################
    ### Step 3: CLEAN ###
    #####################

    # Re-image and clean the data.

    if do_clean:
        print "--------------"
        print "STEP #3: CLEAN"
        print "--------------"

        ### Remove previous versions ###
        os.system('rm -rf '+out_root+'.clean*')

        ### If supplied, read a clean mask ###
        if clean_mask_fits != "":
            print "... importing the clean mask"
            importfits(fitsimage=clean_mask_fits,
                       imagename=out_root+'.clean_mask',
                       overwrite=True)
            clean_mask = out_root+'.clean_mask'

        ### Clean ###
        print "... cleaning"
        clean(vis=out_root+'.ms', imagename=out_root+'.clean',
              mask = clean_mask,
              restfreq=restfreq, mode='velocity',
              width = deltav, nchan = nchan, start = v0,
              cell=cell, imsize=imsize, weighting=weighting,
              robust = robust, niter=niter, threshold=threshold,
              imagermode=imagermode, multiscale=multiscale, pbcor=pbcor,
              interpolation='cubic')

    ######################
    ### Step 4: EXPORT ###
    ######################

    # Export the data to a .fits cube.

    if do_export:
        print "---------------"
        print "STEP #4: EXPORT"
        print "---------------"

        ### Default output file name ###
        if (out_fits_root == None):
            out_fits_root = out_root

        ### Export the clean image
        exportfits(imagename=out_root+'.clean.image',
                   fitsimage=out_fits_root+'.fits', overwrite=True,
                   velocity=True, dropstokes=True)

        ### Export the residuals for the cleaned cube
        exportfits(imagename=out_root+'.clean.residual',
                   fitsimage=out_fits_root+'.resid.fits', overwrite=True,
                   velocity=True, dropstokes=True)

        ### Export the primary beam image for the cleaned cube
        exportfits(imagename=out_root+'.clean.flux',
                   fitsimage=out_fits_root+'.flux.fits', overwrite=True,
                   velocity=True, dropstokes=True)

        ### Export the dirty image
        exportfits(imagename=out_root+'.dirty.image',
                   fitsimage=out_fits_root+'.dirty.fits', overwrite=True,
                   velocity=True, dropstokes=True)

            
    ### Wrap up by resetting log file
    casalog.setlogfile(orig_log_file)        
    return
