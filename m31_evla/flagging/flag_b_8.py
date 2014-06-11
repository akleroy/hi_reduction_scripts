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


print "... ... EA05&EA14 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea05&ea14',
         correlation='RR',
         flagbackup=False)

print "... ... bad time range for EA28 LL."
flagdata(vis=vis,
         antenna='ea28',
         timerange='08:16:37.5~08:17:27.5',
         correlation='LL',
         flagbackup=False)

print "... ... EA04&EA19 LL pathological baseline."
flagdata(vis=vis,
         antenna='ea04&ea19',
         correlation='LL',
         flagbackup=False)


# uvdist vs amp
print "... ... EA05&EA25 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea05&ea25',
         correlation='RR',
         flagbackup=False)

# ea07&ea19; ea19&ea24;, ea10&ea19
print "... ... EA07&EA19, EA19&EA24, EA10&EA19  bad baselines."
flagdata(vis=vis,
         antenna='ea07&ea19;ea10&ea19;ea19&ea24',
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

