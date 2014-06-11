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

# from bpcal
print "... ... EA11 bad"
flagdata(vis=vis,
         antenna='ea11',
         flagbackup=False)


print "... ... EA19 bad"
flagdata(vis=vis,
         antenna='ea19',
         flagbackup=False)

#print "... ... EA13&19 RR bad"
#flagdata(vis=vis,
#         antenna='ea13&ea19',
#         correlation='RR',
#         flagbackup=False)


print "... ... bad time range for 3C48."
flagdata(vis=vis,
         timerange='09:40:02.5',
         correlation='',
         flagbackup=False)

print "... ... EA07&EA24 bad."
flagdata(vis=vis,
         antenna='ea07&ea24',
         correlation='',
         flagbackup=False)

print "... ... EA01 bad time range for phasecal."
flagdata(vis=vis,
         antenna='ea01',
         timerange='10:10:32.5',
         correlation='',
         flagbackup=False)

#print "... ... EA05&EA14 bad time range for phasecal."
#         timerange='12:08:47.5~12:09:02.5',

print "... ... EA05&EA14 bad."
flagdata(vis=vis,
         antenna='ea05&ea14',
         correlation='',
         flagbackup=False)



#print "... ... EA19&EA07 bad."
#flagdata(vis=vis,
#         antenna='ea07&ea19',
#         correlation='',
#         flagbackup=False)


#print "... ... EA19&EA24 bad."
#flagdata(vis=vis,
#         antenna='ea24&ea19',
#         correlation='',
#         flagbackup=False)


# ea07&19 for both correlation?
# ea19 has some problems

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


# final note
# need to flag the low points in uvdist vs amp??
# changed my mind to flag all the EA19's..
# Let's see how does this work. 
