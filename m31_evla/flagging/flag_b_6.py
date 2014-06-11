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
print "... ... EA13 spw 0~7 bad antenna."
flagdata(vis=vis,
         antenna='ea13',
         spw='0~7',
         correlation='',
         flagbackup=False)

# uvdist vs amp
print "... ... EA05&EA14 RR bad baseline."
flagdata(vis=vis,
         antenna='ea05&ea14',
         correlation='RR',
         flagbackup=False)


print "... ... EA04&EA24, EA10&EA24, EA07&EA24  bad baselines."
flagdata(vis=vis,
         antenna='ea04&ea24;ea10&ea24;ea07&ea24',
         correlation='',
         flagbackup=False)


# time vs amp, and a lot of bad baselines with EA19
print "... ... EA19 bad"
flagdata(vis=vis,
         antenna='ea19',
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
