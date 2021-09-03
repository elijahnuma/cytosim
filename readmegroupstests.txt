Groups were batches of tests that I ran together.
Groups before group 6 are groups that I ran before I had a codified system of describing them.
'Tests': the test numbers that correspond to each group
'Group Name': group information (usually information that can't be conveyed through the other information)
'Motor Type': the motor type (rod or point model)
'Motor Counts': the motor counts that span the group
'Variable Name': variable that is tested (head count or stall force)
'Variable List': variable values that span the group
'Binding Ranges (um): binding range values that span the group
'Time Frames (s)': time slices in the simulation that the data recorded from
'Simulation Time (s)': in-simulation run time
'Number of Simulations': number of simulations ran (tests are averaged over this)
The groups are ordered in a loop for the motor lists then a list of the variables. For example: tests 74 
through 79 are all 100 motors but span "2, 4, 6, 8, 16, 32" heads, then tests 80 through 85 are 
all 200 motors but span "2, 4, 6, 8, 16, 32" heads, and so on until the motor list is exhausted.
The messages and outs folders refer to the group's messages.cmo and out.txt files.
Messages and outs were grabbed in the order that they were submitted as jobs.
This means the files are ordered in a loop for the motor lists then a list for the variables then
each simulation individually then each binding range. For example: messages0-9.cmo are all 100 motors,
2 heads, and the same simulation, but span the binding ranges 
"0.001, 0.004, 0.007, 0.01, 0.04, 0.07, 0.1, 0.4, 0.7, 1.0". messages10-19.cmo are all 100 motors,
2 heads, but the next simulation, and span the binding range, and so on until the simulations are exhausted. 
Then this cycle repeated until the variables are exhausted then another cycle starts until the motor list 
is exhausted.
To double check the math, one can multiply the number of binding ranges by the number of simulations by the
number of head counts by the number of motor counts and achieve the number of messages in a given group.

Tests before test 74 are tests that I performed before I had a codified system of describing them.
Each number in each test folder is a different simulation of the same test.
Data_Files contains Cdata.csv, Pdata.csv, Rdata.csv, and tdata.csv.
reports contains the report files for each test, corresponding repsectively to the binding ranges.
I still have saved what the test was performed for under legacy in cytosiminformation.txt but it's difficult to 
understand so if one has trouble deciphering it, let me know, but they were not very important tests in any case.