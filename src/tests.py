import os
import sys
from main import main

print("Arguments: ")
for i in sys.argv:
    print(f"Arg: {i}")

if len(sys.argv) != 2:
    print('No test dir specified')
    exit(1)

dirstr = sys.argv[1]
target = "../build/"

# test dir to absolute path
dirstr = os.path.abspath(dirstr)
target = os.path.abspath(target)

print(f"Test file dir: {dirstr}")
print(f"Target: {target}")

directory = os.fsencode(dirstr)

("\n\n----Test files----")
for file in os.listdir(directory):
    print(f"Test file: {os.fsdecode(file)}")

for file in os.listdir(directory):
    args = [sys.argv[0], 'tests/' + os.fsdecode(file), 'tests/' + target]
    main(args)
