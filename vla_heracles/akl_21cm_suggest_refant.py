"""
NAME

akl_21cm_suggest_refant

DESCRIPTION

Routines to suggest a reference antenna for archival VLA 21cm data
sets in CASA.

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

###################################
### Suggest a reference antenna ###
###################################

def suggest_refant(
    vis = None,
    min_sep = 50.0,
    flag_thresh = 0.1,
    ):
    """
    NAME

    suggest_refant

    DESCRIPTION

    Suggest a reference antenna.

    REQUIRED INPUTS and DEFAULTs
    
    vis (None) : vis

    OPTIONAL INPUTS and DEFAULTs

    COMMENTS and FUTURE

    HISTORY

    Adapted from script by Miriam Krauss - Jun 2010

    Written - aleroy@nrao.edu - Sep 2010
    
    """

    import numpy
    import math

    ### Defaults and error checking ###

    if (vis == None):
        print "Must specify visibility [vis=]. Returning."
        return

    ### Begin ###
    
    print "----------- suggest_refant begins -----------"

    ### Extract antenna information from the MS ###

    tb.open(vis+'/ANTENNA')
    ant_station = tb.getcol('STATION')
    ant_name = tb.getcol('NAME')
    ant_pos = tb.getcol('POSITION')
    tb.close()

    ### Map antennas to stations ###

    mean_x = numpy.mean(ant_pos[0,])
    mean_y = numpy.mean(ant_pos[1,])

    x_offset = ant_pos[0,] - mean_x
    y_offset = ant_pos[1,] - mean_y    
    offset = numpy.sqrt(x_offset**2 + y_offset**2)

    ### Use the flagging tool to get the flagging statistics on each antenna ###

    fg.clearflagselection(0)
    fg.open(vis)
    fg.setdata()
    fg.setflagsummary()
    flag_statistics = fg.run()
    fg.done()

    # sort ot get the fraction flagged by antenna
    frac_flagged_by_ant = 0.0*offset
    for i in range(0,len(ant_name)):
        flagged = float(flag_statistics['antenna'][ant_name[i].upper()]['flagged'])
        total = float(flag_statistics['antenna'][ant_name[i].upper()]['total'])
        frac_flagged = float(flagged/total)
        frac_flagged_by_ant[i] = frac_flagged

    # sort by distance
    ind_by_dist = numpy.argsort(offset)

    # make arrays of criteria
    ant_name = ant_name[ind_by_dist]
    offset = offset[ind_by_dist]
    flagged = frac_flagged_by_ant[ind_by_dist]

    # indices
    suggest_ind = ((offset > min_sep) & (flagged < (flag_thresh+1.0)*numpy.mean(flagged))).nonzero()

    # extract array
    suggest_ind = suggest_ind[0]

    if (suggest_ind == []):
        print "No antennas meet both the flagging and separation criteria."
    else:
        print "Shortest baseline above minimum above flagging threshold: ", ant_name[suggest_ind.min()]

    print "----------- sugggest_refant ends -----------"
    
    return

