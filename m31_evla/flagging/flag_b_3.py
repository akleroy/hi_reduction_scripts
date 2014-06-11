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


print "... ... EA28 LL bad "  #for a certain time range"#timerange='16:30:42.5~16:32:12.5',
flagdata(vis=vis,
         antenna='ea28',
         correlation='LL',
         flagbackup=False)

#print "... ... EA13&EA19 RR bad baseline for bpcal."
#flagdata(vis=vis,
#         antenna='ea13&ea19',
#         scan='2',
#         correlation='RR',
#         flagbackup=False)


print "... ... EA13&EA19, EA05&EA12, EA05&EA25, EA05&EA16, EA05&EA07, EA07&EA19, EA05&EA14, EA07&EA24, EA19&EA24 RR bad baseline."
flagdata(vis=vis,
         antenna='ea13&ea19;ea05&ea12;ea05&ea25;ea05&ea16;ea05&ea07;ea07&ea19;ea05&ea14;ea07&ea24;ea19&ea24',
         correlation='RR',
         flagbackup=False)

#print "... ... EA05&EA12 RR bad baseline."
#flagdata(vis=vis,
#         antenna='ea13&ea19',
#         correlation='RR',
#         flagbackup=False)


print "... ... EA04&EA14 bad baseline."
flagdata(vis=vis,
         antenna='ea04&ea14',
         spw='11:38~39',
         flagbackup=False)


print "... ... EA07 bad baselines..."
flagdata(vis=vis,
         antenna='ea07&ea02;ea07&ea04;ea07&ea06;ea07&ea09;ea07&ea15;ea07&ea17;ea07&ea21',
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



