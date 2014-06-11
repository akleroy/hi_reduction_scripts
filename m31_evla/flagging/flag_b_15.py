print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

#print "... ... bad time range for EA25 in spw 8~15."
#flagdata(vis=vis,
#         antenna='ea25',
#         spw='8~15',
#         timerange='07:46:17.5~07:51:07.5',
#         correlation='',
#         flagbackup=False)

print "... ... EA28 LL bad."
flagdata(vis=vis,
         antenna='ea28',
         correlation='LL',
         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:27~32',
         flagbackup=False)


print "... ... HI absorption on bandpass cal."
flagdata(vis=vis,
         field='3C48',
         spw='0:21~25',
         flagbackup=False)
