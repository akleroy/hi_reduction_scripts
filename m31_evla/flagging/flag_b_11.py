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

print "... ... EA04&EA19 LL pathological baseline."
flagdata(vis=vis,
         antenna='ea04&ea19',
         correlation='LL',
         flagbackup=False)


print "... ... EA19&EA24 LL pathological baseline."
flagdata(vis=vis,
         antenna='ea19&ea24',
         correlation='LL',
         flagbackup=False)

# time vs amplitude
print "... ... EA09&EA21 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea09&ea21',
         correlation='RR',
         flagbackup=False)


print "... ... bad time range for 3C48 in spw12."

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:30:02.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:30:32.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:30:42.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:31:02.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:32:02.5~07:32:12.5',
         correlation='',
         flagbackup=False)


flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:32:22.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:32:32.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:32:42.5~07:32:50.0',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:33:52.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:34:42.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:35:02.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:35:27.5',
         correlation='',
         flagbackup=False)

flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:35:57.5',
         correlation='',
         flagbackup=False)



flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:36:02.5~07:36:07.5',
         correlation='',
         flagbackup=False)


flagdata(vis=vis,
         field='3C48',
         spw='12',
         timerange='07:36:37.5~07:36:47.5',
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


# SPW 12 has too high points..
# not sure how to remove these..
