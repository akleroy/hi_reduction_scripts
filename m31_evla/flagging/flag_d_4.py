print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA06 shows no phase coherence."
flagdata(vis=vis,
         antenna='ea06',
         correlation='',
         flagbackup=False)

print "... ... EA22 shows anamolous amplitudes."
flagdata(vis=vis,
         antenna='ea22',
         correlation='',
         flagbackup=False)

print "... ... First scans on 3C48 Noisy."
flagdata(vis=vis,
         timerange='05:09:30~05:10:20',
         flagbackup=False)

print "... ... HI absorption on bpcal"
flagdata(vis=vis,
         field=bpcal,
         spw='0:19~31',
         flagbackup=False)

print "... ... HI absorption on bpcal"
flagdata(vis=vis,
         field=bpcal,
         spw='8:45~63',
         flagbackup=False)
