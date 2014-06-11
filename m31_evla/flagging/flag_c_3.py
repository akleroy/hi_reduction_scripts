print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA05 shows anamolous amplitudes."
print "... ... EA18 shows no phase coherence."
print "... ... EA19 shows anamolous amplitudes."
print "... ... EA23 shows anamolous amplitudes."
print "... ... EA25 shows anamolous amplitudes."
flagdata(vis=vis,
         antenna='ea05,ea16,ea18,ea19,ea23,ea25',
         correlation='',
         flagbackup=False)

print "... ... EA28 shows anamolous amplitudes in Scan 110."
flagdata(vis=vis,
         antenna='ea28',
         correlation='',
         scan='110',
         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:25~35',
         flagbackup=False)

print "... ... low response time range."
flagdata(vis=vis,
         timerange='22:16:00~22:21:00',
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
