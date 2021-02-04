"""
Author: Saurabh Kulkarni
email: skulkarni27@wisc.edu
cslogin: skulkarni27
Made for CS537 SP21
Generates a test handin directory in current dir
"""

import os
import random
from pathlib import Path

handin_dir = "handin"

if __name__ == '__main__':

    assignments = ["p1", "p2", "p3"]
    max_slip_days = 3 #ontime, slip1, slip2, slip3
    codefile = "test.c"


    os.mkdir(handin_dir)
    # 100 students
    for i in range(100):
        login = "csid" + str(i)
        os.mkdir(os.path.join(handin_dir, login))
        for a in assignments:
            #make the directory for pX for this student
            os.mkdir((os.path.join(handin_dir, login, a)))

            #decide how many slip days this student will use for pX
            slip_days_used = random.randint(0, max_slip_days)
            for j in range(max_slip_days + 1):
                if j == 0:
                    final_dir = "ontime"
                else:
                    final_dir = "slip" + str(j)
                # ./handin/csid1/p1/slip1/
                final_dir = os.path.join((os.path.join(handin_dir, login, a, final_dir)))
                os.mkdir(final_dir)

                #is this the folder in which the student will turn in their file?
                if (slip_days_used == j):
                    Path(os.path.join(final_dir, codefile)).touch()


