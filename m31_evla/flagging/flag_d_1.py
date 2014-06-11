print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

print "... ... bad antennas"
flagdata(vis=vis,
         antenna='ea07,ea18',
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
