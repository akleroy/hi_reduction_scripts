print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA05,EA06,EA23 have anamolous response.."
print "... ... EA18,EA21,EA28 missing."
print "... ... EA19 fairly noisy. Dicey but flagging."
flagdata(vis=vis,
         antenna='ea05,ea06,ea18,ea19,ea21,ea23,ea28',
         correlation='',
         flagbackup=False)

print "... ... EA13&EA14 shows interference."
flagdata(vis=vis,
         antenna='ea13&ea14',
         correlation='',
         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:25~35',
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
