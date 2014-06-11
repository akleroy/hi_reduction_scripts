print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA05,EA23 have noisy amplitude response."
flagdata(vis=vis,
         antenna='ea05,ea21,ea23',
         correlation='',
         flagbackup=False)

print "... ... Noisy baselines EA13&EA19, EA07&EA19, EA19&EA25."
flagdata(vis=vis,
         antenna='ea13&ea19;ea07&ea19;ea19&ea25',
         correlation='',
         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:25~35',
         flagbackup=False)

print "... ... pathological response on bandpass calibrator (debatable)."
flagdata(vis=vis,
         antenna='ea15,ea25',
         flagbackup=False)

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
