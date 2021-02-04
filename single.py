"""
Author: Saurabh Kulkarni
email: skulkarni27@wisc.edu
cslogin: skulkarni27
Made for CS537 FA20
"""

from roster import parseRoster
import os
from partnerClasses import *

rosterFile = "roster.txt"
#handin_dir = "/u/c/s/cs537-1/handin"
# this is the test handin folder, included in the repo
handin_dir = "handin"


#csidToName = parseRoster(rosterFile)

ORDER_BY_LAST_NAME = True


class Status:
    # parsed[0] is a code indicating the status of partner.txt
    def __init__(self, csid, proj_path, required_files):
        self.csid = csid
        #dive into this person's handin for proj
        #subdir = ontime, slip1, etc

        #these are the 3 values associated with each student
        #and their default values
        self.slip_days_used = 0
        self.has_all_required = True
        self.has_extra = False
        self.hasSubmission = False

        #assumes that there are no directories in handin besides
        #ontime, slip1, etc.
        for slip_days, subdir in enumerate(os.listdir(proj_path)):
            subdir = os.path.join(proj_path, subdir)
            if not os.path.isdir(subdir):
                #this should NOT happen
                continue
            submitted_files = []
            for file in os.listdir(subdir):
                submitted_files.append(file)
            if submitted_files:
                #reset the file checks with every late day
                self.has_all_required = True
                self.has_extra = False
                self.hasSubmission = True

                # assumes that the order listdir gives is ontime, slip1, slip2
                self.slip_days_used = slip_days

                # did they submit any extra files?
                for sub in submitted_files:
                    if sub not in required_files:
                        self.has_extra = True
                # did they submit all the required files?
                for req in required_files:
                    if req not in submitted_files:
                        self.has_all_required = False

    def __str__(self):
        outstring = str(csid) + ": "
        if self.hasSubmission:
            outstring += "Has submission. "
        else:
            outstring += "No submission."
            return outstring
        outstring += "Used {:d} slip days. ".format(self.slip_days_used)
        if not self.has_all_required:
            outstring += "Missing file(s). "
        if self.has_extra:
            outstring += "Has extra file(s)."
        return outstring


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Error. Need proj name. Example: p2 or proj2")
        exit(1)

    # pass in required files as such:
    #python single.py p1 my-look.c my-rev.c
    required_files = []
    for i in range(2, len(sys.argv)):
        required_files.append(sys.argv[i].strip())

    proj = sys.argv[1]

    # this is a list of all the cids we've seen
    csid_List = []
    # this dictionary maps each csid to their submission status
    csidToStatus = {}

    # for each handin folder
    for csid in os.listdir(handin_dir):
        proj_path = os.path.join(handin_dir, csid, proj)

        # if we encounter a random file, skip it
        # just looking for handin directories
        if not os.path.isdir(proj_path):
            continue

        # default name = csid
        name = csid
        csid_List.append(csid)
        csidToStatus[csid] = Status(csid, proj_path, required_files)





    # OK We have determined all the groups. Now we just have to print them

    # sort by name
    csid_List = sorted(csid_List)
    seen = set([])
    for csid in csid_List:
        if csid in seen:
            continue

        seen.add(csid)

        status = csidToStatus[csid]

        print(status)



