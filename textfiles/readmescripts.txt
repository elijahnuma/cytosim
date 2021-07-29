name of .cym files should be a descriptor of what is changing in each simulations or a description of the test

/cyms/

cymscheck.sh:
checks if test files were loaded successfully;
args: starting test, ending test

copysims.sh (run in test dir):
copies test files for however many simulations needed;
args: simulation number

deletetests.sh:
deletes range of test folders;
args: starting test, ending test

edit.sh:
edits config files;
args: text to be replaced, replacing text, file name

jobsclear.sh:
clears job files

maketest.sh: 
creates new folder given .cym file;
args: cym file name, simulation number

preconfigs.sh (run in test dir):
looks for templete .cym files and runs pre_config_JMB.py for each folder in current directory

runjobs.sh (run in test dir):
goes into every folder in current directory and runs submit job as a separate job for that folder

/cyms/motortemplates/

flexible.cym:
flexible rod template

*maketest.sh:
runs maketest.sh for each motormodel.cym template, requires modification of for loop to specify motor count

pointdiffusion.cym:
point diffusion template

roddiffusion.cym:
rod diffusion template

stallforce.cym:
point motor template

/datacollection/

checksrecordoffclear.sh:
clears checks and recordoff folders

failedjobscheck.sh:
runs CheckSims.py on jobs and compiles results in checks folder

finishedcheck.sh:
scans checks folder for failed jobs;
args: checks folder number

jobdatafilescheck.sh:
checks if runrecordoff.sh has properly loaded Data_Files, run after submitting recordoff.py, 
generates failedjobs.txt with array of failed jobs;
args: starting job, ending job    
                                                                               
jobdatafilesclear.sh
clears Data_Files folders in jobs 

metadatacollect.sh:
collects metadata from job files

movejobs.sh:
moves new jobs created from rerunjobs.sh to appropriate place in job order, uses jobs from failedjobs.txt;

pendingrunningjobs.sh:
checks running and pending jobs in bjobs

recordoff.py:
creates Data_Files for job number

rerunjobs.sh:
re-runs job by re-reunning entire test and respective jobs, uses jobs from failedjobs.txt;

runsubmitrecordoff.sh:
creates readable data files in job folders without data file;

submitfailedjobscheck.csh:
submits failedjobscheck.sh

submitrecordoff.csh:
submits recordoff.py

/datacollection/data/

analyzejobs.sh: 
puts respective jobs into respective folders;
args: test folder, starting job, ending job, report name (point/rod) 

datacheck.sh:
checks if Data_Files was successfully copied and reports was loaded successfully;
args: starting job, ending jobs

dataclear.sh:
clears test folders;
args: starting test, ending test

runanalyzejobs.sh:
runs analyzejobs.sh for successive job batches by accessing submitanalyzejobs.csh;
args: starting test folder, ending test folder, report type;
report types: "pointcom", "pointattach", "rodcom", "rodattach"

submitanalyzejobs.csh:
submits analyzejobs.sh to cluster

/metadata/

getmessagescmo.sh (run in messages folder):
copies messages.cmo files from jobs

getoutstxt.sh (run in outs folder):
copies outs.txt files from jobs

how to run simulations:
maketest.sh -> failedjobscheck.sh -> finishedcheck.sh -> runsubmitrecordoff.sh -> jobdatafilescheck.sh ->
rerunjobs.sh -> failedjobscheck.sh -> finishedcheck.sh -> runsubmitrecordoff.sh -> movejobs.sh -> 
runanalyzejobs.sh -> datacheck.sh -> metadatacollect.sh -> sftp -> get

/gitrepo/

copyscripts.sh:
copies scripts and text files from all other folders to send to repository

git workflow:
bash copyscripts.sh -> git add -A -> git commit -m "message" -> git push
