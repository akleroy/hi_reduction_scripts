print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)


print "... ... EA10 bad"
flagdata(vis=vis,
         antenna='ea10',
         correlation='',
         flagbackup=False)


print "... ... EA15 bad in spw 8~15."
flagdata(vis=vis,
         antenna='ea15',
         spw='8~15',
         correlation='',
         flagbackup=False)

print "... ... EA18 LL bad in spw 0~7 in scan2."
flagdata(vis=vis,
         antenna='ea18',
         spw='0~7',
         scan='2',
         correlation='LL',
         flagbackup=False)


# time vs amp
print "... ... EA26, EA07 bad in certain timerange for 3c48."
flagdata(vis=vis,
         field='3C48',
         antenna='ea26,ea07,ea27',
         timerange='11:57:02.5',
         correlation='',
         flagbackup=False)

print "... ... EA16 bad in certain timerange for 3c48."
flagdata(vis=vis,
         field='3C48',
         antenna='ea16',
         timerange='11:56:57.5',
         correlation='',
         flagbackup=False)


print "... ... EA19 bad in certain timerange for 3c48."

flagdata(vis=vis,
         field='3C48',
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
