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


# from bpcal....
print "... ... EA01 bad for spw 0~7"
flagdata(vis=vis,
         antenna='ea01',
         spw='0~7',
         timerange='09:50:57.5~09:52:32.5',
         flagbackup=False)


print "... ... EA07&EA19 LL bad baseline for spw 0~7"
flagdata(vis=vis,
         antenna='ea07&ea19',
         spw='0~7',
         correlation='LL',         
         flagbackup=False)


print "... ... EA13&EA19 RR bad baseline"
flagdata(vis=vis,
         antenna='ea13&ea19',
         correlation='RR',         
         flagbackup=False)

#upto here..

#uvdist vs amp

print "... ... EA04&EA14, EA05&EA14, EA05&EA25, EA04&EA05 bad baseline"
flagdata(vis=vis,
         antenna='ea04&ea14;ea05&ea14;ea05&ea25;ea04&ea05',
         flagbackup=False)



#print "... ... EA04&EA14 bad baseline"
#flagdata(vis=vis,
#         antenna='ea04&ea14',
#         scan='57,70,83,96,110',
#         flagbackup=False)

#print "... ... EA05&EA14 bad baseline"
#flagdata(vis=vis,
#         antenna='ea05&ea14',
#         flagbackup=False)

#print "... ... EA05&EA25 bad baseline"
#flagdata(vis=vis,
#         antenna='ea05&ea25',
#         scan='70,83,96,110',
#         flagbackup=False)

#print "... ... EA04&EA05 bad baseline"
#flagdata(vis=vis,
#         antenna='ea04&ea05',
#         scan='96,110',
#         flagbackup=False)




#time vs amp
print "... ... EA28 LL fluctuating amp & phase for bpcal"
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
