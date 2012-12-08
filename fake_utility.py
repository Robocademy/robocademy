#fake_utility.py, just generates lots of output over time
import sys, time
for i in range(10):
   print i
   sys.stdout.flush()
   time.sleep(0.5)
