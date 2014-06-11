print "... ... edge channels"
flagdata(vis=vis,
         spw='0~15:0~10;53~63',
         flagbackup=False)

#flagdata(vis=vis,
#         antenna='ea06,ea18,ea19,ea05,ea23',
#         correlation='',
#         flagbackup=False)

print "... ... HI absorption on phasecal."
flagdata(vis=vis,
         field='J0029+3456',
         spw='0:25~35',
         flagbackup=False)

# EA05 and EA23 both look terrible on LL
print "... ... EA05 and EA23 both show noisy LL polarizations."
flagdata(vis=vis,
         antenna='ea23',
         correlation="LL",
         flagbackup=False)

print "... ... EA13 shows recurring RFI."
flagdata(vis=vis,
         antenna='ea13',
         correlation="RR",
         flagbackup=False)

print "... ... EA13&EA14 problematic baseline."
flagdata(vis=vis,
         antenna='ea13&ea14',
         correlation="LL",
         flagbackup=False)

print "... ... EA02 shows phase issues."
flagdata(vis=vis,
         antenna='ea02',
         flagbackup=False)

print "... ... EA05 has lots of issues (RFI, weak response, etc.)."
flagdata(vis=vis,
         antenna='ea05',
         flagbackup=False)

print "... ... EA19&EA22 bad baseline in scan 30."
flagdata(vis=vis,
         antenna='ea19&ea22',
         scan='30',
         flagbackup=False)


#print "... ... EA05&EA13 - bad RFI spike"
#flagdata(vis=vis,
#         antenna='ea05&ea13',
#         flagbackup=False)

#print "... ... EA05&EA07 - low amps in scan 30"
#flagdata(vis=vis,
#         antenna='ea05&ea07',
#         scan='30',
#         flagbackup=False)

#print "... ... EA13&EA14 - RFI"
#flagdata(vis=vis,
#         antenna='ea13&ea14',
#         flagbackup=False)


# ... EA23 shows very low response on one or more SPW/pols
# ... EA28 shows a spike at a few times... RFI?

# EA05&EA07 in scan 30 - low amps
# scan 17 - low amps throughout
# EA05&EA13 bad RFI - many scans

print "... ... HI absorption on bpcal."
flagdata(vis=vis,
         field=bpcal,
         spw='0:17~30',
         flagbackup=False)

flagdata(vis=vis,
         field=bpcal,
         spw='8:45~63',
         flagbackup=False)
