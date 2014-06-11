print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)


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

#### need to confirm this later
print "... ... EA04&EA19 LL bad baseline."
flagdata(vis=vis,
         antenna='ea04&ea19',
         correlation='LL',
         flagbackup=False)

print "... ... EA13 spw 0~7 bad antenna."
flagdata(vis=vis,
         antenna='ea13',
         spw='0~7',
         correlation='',
         flagbackup=False)


print "... ... EA11&EA19, EA11&EA24, EA24&EA19 bad baseline."
flagdata(vis=vis,
         antenna='ea11&ea19;ea11&ea24;ea24&ea19;ea10&ea24;ea07&ea19;ea07&ea24',
         correlation='',
         flagbackup=False)


# uvdist vs amp
print "... ... EA05&EA14 RR bad baseline."
flagdata(vis=vis,
         antenna='ea05&ea14',
         correlation='RR',
         flagbackup=False)

print "... ... EA12 bad"
flagdata(vis=vis,
         antenna='ea12',
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



