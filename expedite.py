import subprocess
import sys
# run all my programs in sequence

prefix = sys.argv[1]
size = sys.argv[2]

#generate demographics
subprocess.run(['python', 'demogenerator.py', prefix + '_demomap', size])

#convert to json
subprocess.run(['python', 'toymap.py', prefix + '_demomap.csv', prefix + '_demomap', size])

#create partitions
subprocess.run(['python', 'gchain.py', prefix + "_demomap.json", prefix + "_pnd.csv"])

#combine demographics with partitions
subprocess.run(['python', 'dist_part_sum.py', prefix + '_pnd.csv', prefix + '_demomap.csv', prefix + '_pd'])

#get entropy
subprocess.run(['python', 'get_entropy.py', prefix + '_pd', prefix + '_ecd', '1'])
subprocess.run(['python', 'get_entropy.py', prefix + '_pd', prefix + '_edc', '0'])