preconfigs.sh (run in test dir)
looks for templete .cym files and runs pre_config_JMB.py for each folder in current directory

editconfigs.sh
edits config files, args: text to be replaced, replacing text, file name

copysims.sh (run in test dir)
copies test files for however many simulations needed, args: simulation number

runjobs.sh (run in test dir)
goes into every folder in current directory and runs submit_lsf.py as a separate job for that folder

maketest.sh (run in cyms dir)
creates new folder given .cym file, args: cym file name

copytest.sh (run in cyms dir)
copies .cym file from selected test and changes .cym file, args: test copy, target text, replacement text

submitrecordoff.sh (run in datacollection dir)
creates readable data files in each job folder, args: starting job, ending job

analyzejobs.sh (run in data dir)
puts respective jobs into respective folders, args: test folder, job to start on, job to finish on

deletetest.sh (run in cyms dir)
deletes gives test folder, args: test folder

how to run simulations:
bash copytest.sh/maketest.sh -> bash submitrecordoff.sh -> bash collectjobs.sh -> sftp -> get
