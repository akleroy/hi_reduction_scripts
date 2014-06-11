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

print "... ... EA04 bad"
flagdata(vis=vis,
         antenna='ea04',
         correlation='',
         flagbackup=False)

print "... ... EA19 bad for 3C48"
flagdata(vis=vis,
         antenna='ea19',
         field='3C48',
         correlation='',
         flagbackup=False)


print "... ... EA05&EA14 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea05&ea14',
         correlation='RR',
         flagbackup=False)

#uvdist vs amp
print "... ... EA05&EA25 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea05&ea25',
         correlation='RR',
         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:27~32',
         flagbackup=False)


print "... ... HI absorption on bpcal."
flagdata(vis=vis,
         field='3C48',
         spw='0:21~25',
         flagbackup=False)

# definetley need to come back later

