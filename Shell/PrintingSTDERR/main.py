import sys
for i in range(10):
    if i == 2:
        print("CIAO SU STDERR",file=sys.stderr,flush=True)
    else:
        print("CIAO SU STDOUT",flush=True)