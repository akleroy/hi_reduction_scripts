print "... ... edge channels."
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA05, EA23 have pathological amplitudes."
flagdata(vis=vis,
         antenna='ea05,ea23',
         correlation='',
         flagbackup=False)

print "... ... EA13 pathological amplitudes."
flagdata(vis=vis,
         antenna='ea13',
         correlation='',
         flagbackup=False)

print "... ... EA19&EA25 pathological baseline."
flagdata(vis=vis,
         antenna='ea19&ea25',
         correlation='',
         flagbackup=False)

print "... ... pathological response on bandpass calibrator (debatable)."
flagdata(vis=vis,
         antenna='ea15,ea25',
         flagbackup=False)

print "... ... bad time range."
flagdata(vis=vis,
         timerange='23:40:30~23:42:30',
         correlation='',
         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:25~35',
         flagbackup=False)

# could do more agressive flagging on the first part of the data. That
# time range shows signatures of a bunch of RFI.

print "... ... HI absorption on bpcal."
flagdata(vis=vis,
         field=bpcal,
         spw='0:17~29',
         flagbackup=False)

print "... ... HI absorption on bpcal."
flagdata(vis=vis,
         field=bpcal,
         spw='8:45~63',
         flagbackup=False)
