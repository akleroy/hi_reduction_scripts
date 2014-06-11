print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

# inspection of caltables...

# BP cal
# 1) short timescale phase variability (.bpphase)
# ea15 : shows jumps in phase at three different times
# ea23, 26 : quite noisy phase varaitions as a function of time

# 2) phase vs freq okay

# 3) amp vs freq
# ea05, ea23, ea26 up to 6% variation.

# 4) amp vs channel : looks okay

# Gaincal
# What should I look for here??
# 5) scanphase vs time
# 6) flux vs time

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

print "... ... EA04&EA19 LL pathological baseline."
flagdata(vis=vis,
         antenna='ea04&ea19',
         correlation='LL',
         flagbackup=False)

print "... ... EA05&EA25 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea05&ea25',
         correlation='RR',
         flagbackup=False)

print "... ... EA05&EA14 RR pathological baseline."
flagdata(vis=vis,
         antenna='ea05&ea14',
         correlation='RR',
         flagbackup=False)


print "... ... bad time range for EA15."
flagdata(vis=vis,
         antenna='ea15',
         timerange='09:21:12.5~09:21:17.5,09:19:22.5',
         correlation='',
         flagbackup=False)



# uvdist vs amp
# ea07&ea19; ea07&ea24; ea19&ea24; ea10&ea24, ea10&ea19
print "... ... EA07&EA19, EA07&EA24, EA10&EA24, EA19&EA24, EA10&EA19  bad baselines."
flagdata(vis=vis,
         antenna='ea07&ea19;ea07&ea24;ea10&ea24;ea10&ea19;ea19&ea24',
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
