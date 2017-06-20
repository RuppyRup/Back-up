
import sys

platform = sys.platform

if platform == "linux" or platform == "linux2":
   # linux
   print('Linux')
elif platform == "darwin":
   # MAC OS X
   print('Mac')        
elif platform == "win32":
   # Windows
   print('Windows')
