name of .cym files should be a descriptor of what is changing in each simulations or a description of the test

/cyms/

backup.sh (RUN ONLY IN LOGIN cyms/ DIR):
backs up share folder

cymscheck.sh:
checks if test files were loaded successfully;
args: starting test, ending test

copysims.sh (run in test dir):
copies test files for however many simulations needed;
args: simulation number

copytest.sh: 
copies .cym file from selected test and changes .cym file;
args: test copy, target text, replacement text

deletetests.sh:
deletes range of test folders;
args: starting test, ending test

edit.sh:
edits config files;
args: text to be replaced, replacing text, file name

insert.sh:
inserts test into desired location;
args: test to insert, desired test location

jobsclear.sh:
clears job files

maketest.sh: 
creates new folder given .cym file;
args: cym file name, simulation number

preconfigs.sh (run in test dir):
looks for templete .cym files and runs pre_config_JMB.py for each folder in current directory

redotest.sh: 
redoes test;
args: test number, target text, replacement text

runjobs.sh (run in test dir):
goes into every folder in current directory and runs submit job as a separate job for that folder

/cyms/motortemplates/

flexible.cym:
flexible rod template

pointdiffusion.cym:
point diffusion template

pointmaketest.sh:
runs maketest.sh for each stallforce.cym rod template, requires modification of for loop to specify motor count

roddiffusion.cym:
rod diffusion template

rodmaketest.sh:
runs maketest.sh for each #heads.cym rod template, requires modification of for loop to specify motor count

stallforce.cym:
point motor template

/datacollection/

datafilescheck.sh:
checks if runrecordoff.sh has properly loaded Data_Files, run after submitting recordoff.py 
args: starting job, ending job

datafilesclear.sh
clears Data_Files folders in jobs

failedjobscheck.sh:
runs CheckSims.py on jobs and compiles results in checks folder;
args: checks folder number

finishedcheck.sh:
scans checks folder for failed jobs;
args: checks folder number

metadatacollect.sh:
collects metadata from job files

pendingrunningjobs.sh:
checks running and pending jobs in bjobs

recordoffchecksclear.sh:
clears recordoff folders, run after submitting recordoff.py

recordoff.py:
creates Data_Files for job number

runsubmitrecordoff.sh:
creates readable data files in each job folder;
args: recordoffs folder number, starting job, ending job

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
bash copytest.sh OR maketest.sh OR anchormaketest.sh -> bash failedjobscheck.sh -> bash finishedcheck.sh ->
bash runsubmitrecordoff.sh -> bash metadatacollect.sh -> bash runanalyzejobs.sh -> bash datacheck.sh ->
sftp -> get

/gitrepo/

copyscripts.sh:
copies scripts and text files from all other folders to send to repository

git workflow:
bash copyscripts.sh -> git add -A -> git commit -m "message" -> git push
