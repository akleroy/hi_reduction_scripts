print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA18 missing."
print "... ... EA05, EA23 show amplitude/phase jitter."
print "... ... EA06 shows amplitude wraps."
print "... ... EA19 shows interference."
flagdata(vis=vis,
         antenna='ea06,ea18,ea19,ea05,ea23',
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
