"""
NAME

akl_21cm_import

DESCRIPTION

Routines to handle the importing of archival VLA 21cm data sets in
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
              spw = import_spw, field = import_field,
              datacolumn='data')

        # replace original ms with split version
        os.system('rm -rf '+vis)
        os.system('mv '+vis+'.select '+vis)

    ### Run listobs and copy the output to a text file ###
    print "...listobs"

    casapy_util.listobs_to_file(vis,out_root+'.listobs.txt')
    
    ### Save flags with the version tag "imported" ###

    print "...flagmanager"
        
    flagmanager(vis=vis, mode='save', versionname='imported',
                comment='flagging after import', merge='replace')

    ### Finish ###
    print "------------ import_21cm ends ------------"

    # set log back to its original value
    casalog.setlogfile(orig_log_file)

    return
