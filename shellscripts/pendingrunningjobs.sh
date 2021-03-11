echo JOB BATCH STARTED: $(bjobs | grep -oe '[A-Za-z]*[[:space:]]*[0-9]* [0-9]*:[0-9]*' | head -n 1)
echo PENDING: $(bjobs | grep "PEND" | wc -l)
echo RUNNING: $(bjobs | grep "RUN" | wc -l)
