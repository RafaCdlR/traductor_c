import os
import sys
from main import main

if len(sys.argv != 3):
    print('No test dir specified')

dirstr = sys.argv[1]
target = sys.argv[2]

directory = os.fsencode(dirstr)

for file in os.listdir(directory):
    args = [os.fsdecode(file), target]
    main(args)
