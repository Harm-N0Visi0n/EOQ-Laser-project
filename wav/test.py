import os
from random import choice
PATH = "/home/harm/lms/end_of_quarter/EOQ3/EOQ-Laser-project/wav/"
os.system("amixer set Master 180%")
for file in os.listdir(PATH):
    path = os.path.join(PATH, file)
    if os.path.isfile(path) and "test" not in file:
        os.system(f"aplay {path}")
        # print(file)

