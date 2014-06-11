print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA12 LL shows pathological amp. bandpass."
print "... ... (flagging both corrs)"
flagdata(vis=vis,
         antenna='ea12',
         correlation='',
         flagbackup=False)

print "... ... EA07 RR very noisy."
flagdata(vis=vis,
         antenna='ea07',
         correlation='',
         flagbackup=False)

print "... ... EA28 RR very noisy."
flagdata(vis=vis,
         antenna='ea28',
         correlation='',
         flagbackup=False)

print "... ... HI absorption on bpcal"
flagdata(vis=vis,
         field=bpcal,
         spw='0:19~31',
         flagbackup=False)

print "... ... HI absorption on bpcal"
flagdata(vis=vis,
         field=bpcal,
         spw='8:45~63',
         flagbackup=False)
