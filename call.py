import subprocess
proc = subprocess.Popen(['python','fake_utility.py'],stdout=subprocess.PIPE)
#works in python 3.0+
#for line in proc.stdout:
for line in iter(proc.stdout.readline,''):
   print line.rstrip()
