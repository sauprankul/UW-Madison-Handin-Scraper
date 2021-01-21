from enum import Enum
import sys

class ParseCode(Enum):
    good_pair_sub = 1 # 2 partners listed in partner.txt, code exists
    format_error_sub = 2 # code
    good_alone = 3 # txt and submission for 1 person
    none_found_sub = 4
    empty = 5
    no_dir = 6
    format_error_no_sub = 7
    good_pair_no_sub = 8 # 2 partners listed in partner.txt, no code



class ResultCode(Enum):
    good = 1
    miss_txt_sub = 2
    mult_sub = 3
    no_proj = 4
    partial_match = 5
    conflict = 6


class Group:

    # parsed[0] is a code indicating the status of partner.txt
    def __init__(self, name, csid, pcode, partner_info=None):
        self.name1 = name
        self.csid1 = csid
        self.pcode1 = pcode
        self.name2 = None
        self.csid2 = None
        self.pcode2 = None
        self.p1HasSub = self.hasSub()


        # default
        self.rcode = ResultCode.good
        # this person claimed to work alone in their partner.txt
        if self.pcode1 == ParseCode.good_alone:
            self.rcode = ResultCode.good

        elif self.pcode1 == ParseCode.good_pair_sub\
                or self.pcode1 == ParseCode.good_pair_no_sub:
            # until the other partner.txt shows up, this is a partial
            #make this good when other shows up
            self.rcode = ResultCode.partial_match

        # no partner.txt, but with code
        elif self.pcode1 == ParseCode.format_error_sub\
                or self.pcode1 == ParseCode.none_found_sub:
            self.rcode = ResultCode.miss_txt_sub

        elif self.pcode1 == ParseCode.empty\
                or self.pcode1 == ParseCode.no_dir\
                or self.pcode1 == ParseCode.format_error_no_sub:
            self.rcode = ResultCode.no_proj

        else:
            print("Error. due to pcode:" + str(self.pcode1))
            sys.exit()

        #handle the partner information
        if partner_info:
            self.name2 = partner_info[0]
            self.csid2 = partner_info[1]



    def integrate(self, other, partial=False):

        # multiple submissions
        if self.hasSub() and other.hasSub():
            self.rcode = ResultCode.mult_sub

        # 2 people who only turned in partner.txts?
        elif not self.hasSub() and not other.hasSub():
            self.rcode = ResultCode.no_proj


        #so we only have 1 sub between 2 people
        else:
            if partial:
                self.rcode = ResultCode.partial_match
            else:
                self.rcode = ResultCode.good

        self.p1HasSub = self.hasSub() #if p1 has the sub

        if not self.name2:
            self.name2 = other.getName1()
        self.csid2 = other.getcsid1() # reuse the csid that was "real"
        self.pcode2 = other.getPcode1()

        return


    def hasSub(self):
        return self.pcode1 in\
            (ParseCode.good_pair_sub,
             ParseCode.format_error_sub,
             ParseCode.good_alone,
             ParseCode.none_found_sub)\
            or self.pcode2 in\
            (ParseCode.good_pair_sub,
             ParseCode.format_error_sub,
             ParseCode.good_alone,
             ParseCode.none_found_sub)\


    def getcsid1(self):
        return self.csid1

    def getName1(self):
        return self.name1

    def getcsid2(self):
        return self.csid2

    def getName2(self):
        return self.name2

    def getPcode1(self):
        return self.pcode1

    def getPcode2(self):
        return self.pcode2

    def getFinalText(self):
        finalText = ""
        if (self.p1HasSub):
          finalText = self.name1 + " (" + self.csid1 + " has sub)"
        else:
          finalText = self.name1 + " (" + self.csid1 + " doesn't have sub)"

        if self.rcode == ResultCode.good:
            if self.csid2:
                finalText = finalText + ", " + self.name2 + " ("\
                        + self.csid2 + ")"
            return finalText + ": Good"

        elif self.rcode == ResultCode.miss_txt_sub:
            return finalText + ": Found code but BAD partner.txt. Check manually!"

        elif self.rcode == ResultCode.mult_sub:
            #assume p2 exists
            assert self.csid2
            return finalText + ", " + self.name2 + " ("\
                        + self.csid2 + ")" +\
                   ": Found multiple submissions"

        elif self.rcode == ResultCode.no_proj:
            if self.csid2:
                finalText = finalText + ", " + self.name2 + " ("\
                        + self.csid2 + ")"
            return finalText + ": Could not find project"

        elif self.rcode == ResultCode.partial_match:

            #p2 should exist for partial match
            assert self.csid2
            if self.csid2:
                finalText = finalText + ", " + self.name2 + " ("\
                        + self.csid2 + ")"
            return finalText + ": Partial match. Only found one partner.txt"

        # TODO: This never happens. I just ignore this possibility
        elif self.rcode == ResultCode.conflict:
            if self.csid2:
                finalText = finalText + ", " + self.name2 + " ("\
                        + self.csid2 + ")"
            return finalText + ": Conflict. Partner triangle?"

        else:
            return "Error. due to rcode above"

    def __str__(self):
        return self.getFinalText()

    def __repr__(self):
        return str(self.name1) + ", " + str(self.csid1) + ", " + str(self.pcode1)\
            + ", " +  str(self.name2) + ", " + str(self.csid2) + ", " + str(self.pcode2) + "\n"






