"""
Author: Saurabh Kulkarni
email: skulkarni27@wisc.edu
cslogin: skulkarni27
Made for CS537 FA20
"""

from roster import parseRoster
import sys
import os
from partnerClasses import *

rosterFile = "roster.txt"
#handin_dir = "/u/c/s/cs537-1/handin"
# this is the test handin folder, included in the repo
handin_dir = "handin"

# for testing
#handin_dir = "./handin"

csidToName = parseRoster(rosterFile)

ORDER_BY_LAST_NAME = True

# takes stuff like:
# netID: skulkarni
# and returns
# skulkarni
def stripLeftOfColon(mystr):
    mystr = mystr.split(":")
    if len(mystr) == 2:
        return mystr[1].strip()
    else:
        return mystr[0].strip()

# toParse = "lastname, firstname" or "firstname lastname"
def parseName(toParse, default):
    toParse = toParse.split(',')

    if ORDER_BY_LAST_NAME:

        #["lastname, "firstname"]
        if len(toParse) == 2:
            return toParse[0] + ", " + toParse[1]
        #["firstname lastname"]
        elif len(toParse) == 1:
            toParse = toParse[0].split(" ")
            if len(toParse) == 2:
              return toParse[1] + ", " + toParse[0]
            else:
              return toParse[0]
        else: #wtf
            return default

    else:
        #["lastname, "firstname"]
        if len(toParse) == 2:
            return toParse[1] + " " + toParse[0]
        #["firstname lastname"]
        elif len(toParse) == 1:
            toParse = toParse[0].split(" ")
            if len(toParse) == 2:
              return toParse[0] + " " + toParse[1]
            else:
              return toParse[0]
        else: #wtf
            return default


# sub = True means there was a submission in this dir
# format:
# lastname, firstname, csid, wiscid
# or:
# firstname lastname, csid, wiscid
def parseLines(name, csid, txt, sub):
    fp = open(txt, "r")
    lines = fp.readlines()
    fp.close()

    #empty file
    if len(lines) == 0 or len(lines) > 2:
        #print("too few or too many lines")
        if sub:
            return Group(name, csid, ParseCode.format_error_sub)
        else:
            return Group(name, csid, ParseCode.format_error_no_sub)

    #solo
    if len(lines) == 1 or len(lines[1]) < 2:
        p1 = [stripLeftOfColon(x.strip()) for x in lines[0].rsplit(',', 2)]

        #not enough tokens in this line
        if len(p1) != 3:
            #format error
            if sub:
                return Group(name, csid, ParseCode.format_error_sub)
            else:
                return Group(name, csid, ParseCode.format_error_no_sub)
        #looks good, solo
        else:
            # my name was not found in roster
            # possibly because there is no roster.tx
            # let's just pull the name from the partner.txt then
            if name == csid:
                name = parseName(p1[0], name)
            return Group(name, csid, ParseCode.good_alone)

    #assuming not solo
    p1 = [stripLeftOfColon(x.strip()) for x in lines[0].rsplit(',', 2)]
    p2 = [stripLeftOfColon(x.strip()) for x in lines[1].rsplit(',', 2)]
    ps = (p1, p2)

    #check number of tokens
    if len(p1) != 3 or len(p2) != 3:
        if sub:
            return Group(name, csid, ParseCode.format_error_sub)
        else:
            return Group(name, csid, ParseCode.format_error_no_sub)

    my_index = -1
    partner_index = -1
    if csid in ps[0]:
        my_index = 0
        partner_index = 1
    else: #csid in ps[1]
        my_index = 1
        partner_index = 0

    partner_csid = ps[partner_index][1]

    # my name was not found in roster
    # possibly because there is no roster.tx
    # let's just pull the name from the partner.txt then
    if name == csid:
        name = parseName(ps[my_index][0], name)
    # check if csid was in roster.txt
    if partner_csid in csidToName:
        partner_name = csidToName[partner_csid]
        if partner_name == partner_csid:
            partner_name = parseName(ps[partner_index][0], "")

    else: # the csid mentioned in this partner.txt is not in the roster
        # attempt to scrape from partner.txt
        partner_name = parseName(ps[partner_index][0], "")
        # returned default
        if partner_name == "":
            if sub:
                return Group(name, csid, ParseCode.format_error_sub)
            else:
                return Group(name, csid, ParseCode.format_error_no_sub)

    if sub:
        return Group(name, csid, ParseCode.good_pair_sub,
                 (partner_name, partner_csid))
    else:
        return Group(name, csid, ParseCode.good_pair_no_sub,
                     (partner_name, partner_csid))

def parseTxt(proj_path, name, csid):
    try:
        file_list = os.listdir(proj_path)

        if "partner.txt" not in file_list:
            # no sub
            if len(file_list) == 0:
                return Group(name, csid, ParseCode.empty)
            # sub but no txt
            else:
                return Group(name, csid, ParseCode.none_found_sub)

        # there is a partner.txt
        else:
            txt_path = os.path.join(proj_path, "partner.txt")

            # was there a submission beyond the partner.txt?
            sub = len(file_list) > 1
            parsed = parseLines(name, csid, txt_path, sub)

            return parsed

    except OSError:
        return Group(name, csid, ParseCode.no_dir)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Error. Need proj name. Example: proj2")
        exit(1)
    proj = sys.argv[1]

    # this is a list of all the cids we've seen
    csid_List = []
    # this dictionary maps each csid to their unique group
    csidToGroup = {None: []}

    # for each handin folder
    for csid in os.listdir(handin_dir):
        proj_path = os.path.join(handin_dir, csid, proj)

        # if we encounter a random file, skip it
        # just looking for handin directories
        if not os.path.isdir(proj_path):
            continue

        # default name = csid
        if csid not in csidToName:
            name = csid
        # we have a roster?
        else:
            name = csidToName[csid]

        newGroup = parseTxt(proj_path, name, csid)

        csidToName[csid] = newGroup.getName1()

        # someone else has claimed this person into their group
        # or if this person is claiming someone we've seen before
        name = newGroup.getName1()
        csid_List.append(csid)
        partner_name = newGroup.getName2()
        partner_csid = newGroup.getcsid2()

        if csid in csidToGroup:
            originalGroup = csidToGroup[csid]

            #let's make sure this person claims the same

            #check if original name = new partner name
            # WARNING: ASSUMING THAT IF ONLY ONE OF THESE HAS A NONE
            # PARTNER, THE OTHER IS CORRECT.
            # We do this by making sure
            # bool(partner of original) XOR bool(partner of new)

            true_match = originalGroup.getName1() == newGroup.getName2()
            partial_match = (bool(originalGroup.getName2()) ^ bool(newGroup.getName2()))
            if (true_match or partial_match):
                #we have a pair... probably
                originalGroup.integrate(newGroup, partial_match)

                #nameToGroup[name] = originalGroup
                csidToGroup[originalGroup.getcsid1()] = originalGroup
                continue

            else:
                #print("conflict :(. Something went really wrong.")
                # weird conflict.
                # we're just gonna pretend that
                # nobody has claimed this person yet
                pass

        # nobody has claimed this person yet
        else:
            # did this person have a valid partner.txt?
            if partner_csid:

                # poor partner doesn't know their name
                # or maybe we just haven't seen this partner yet
                csidToName[partner_csid] = partner_name

                # did we previously see this partner, but they had a bad txt?
                if partner_csid in csidToGroup:
                    # we've seen this partner before!
                    # they must have messed up their partner.txt
                    # let's integrate into the new group
                    # because the new group has a vaid partner.txt
                    originalGroup = csidToGroup[partner_csid]

                    #partial is true because otherwise we'd have matched eariler
                    newGroup.integrate(originalGroup, partial=True)
                    # the csid from the original group might be different??
                    # no, we're literally using the partner csid as a key.
                    #partner_csid = newGroup.getcsid2()


                csidToGroup[csid] = newGroup
                csidToGroup[partner_csid] = newGroup


            # all we need to do is store this group then!
            else:
                csidToGroup[csid] = newGroup



    # OK We have determined all the groups. Now we just have to print them

    # sort by name
    csid_List = sorted(csid_List, key=lambda csid : csidToName[csid])
    seen = set([])
    for csid in csid_List:
        if csid in seen:
            continue

        seen.add(csid)

        group = csidToGroup[csid]

        # this allows us to skip printing partners redundantly
        partner_csid = group.getcsid2()
        if partner_csid == csid:
            partner_csid = group.getcsid1()
        seen.add(partner_csid)

        print(group)



