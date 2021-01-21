import sys


def parseRoster(filename):

    try:
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        csidToName = {}
        # first 2 lines are headers
        for i in range(2, len(lines)):
            line = lines[i]
            # ["lastname, firstname", "wiscID", "csid"]
            line = line.rsplit(maxsplit=2)
            # name : csid
            csidToName[line[2].strip()] = line[0].strip()

        return csidToName

    except OSError:
        return {}
