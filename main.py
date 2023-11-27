from os import listdir
from os.path import isfile,join
files = [f for f in listdir('speeches-20231123') if isfile(join('speeches-20231123', f))]
print (files)