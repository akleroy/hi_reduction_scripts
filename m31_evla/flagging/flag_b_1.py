print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

# recurring dip in second SPW near MW velocities - HI absorption on BPCAL - flag and interpolate?

# ea06 bandpass noiser than others

# ea23 has some issues - one polarization appears bad

# ea26 has some issues - one polarization appears bad



print "... ... EA23 LL bad"
flagdata(vis=vis,
         antenna='ea23',
         correlation='LL',
         flagbackup=False)

print "... ... EA26 RR bad"
flagdata(vis=vis,
         antenna='ea26',
         correlation='RR',
         flagbackup=False)

print "... ... EA06 RR bad"
flagdata(vis=vis,
         antenna='ea06',
         correlation='RR',
         flagbackup=False)


#print "... ... EA06 RR in spw 8~15 for certain time range bad"
#flagdata(vis=vis,
#         antenna='ea06',
#         spw='8~15',
#         timerange='10:35:02.5~10:35:10.0',
#         correlation='RR',
#         flagbackup=False)



# bad time range
print "... ... bad time range for 3C48 in RR."
flagdata(vis=vis,
         timerange='10:35:42.5~10:35:52.5',
         correlation='RR',
         flagbackup=False)

flagdata(vis=vis,
         timerange='10:31:47.5',
         correlation='',
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


