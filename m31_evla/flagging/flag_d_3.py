print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... EA05 missing some SPWs."
flagdata(vis=vis,
         antenna='ea05,ea28',
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
         spw='8:45~*',
         flagbackup=False)
