import sys
import random

if __name__ == '__main__':

    # previous version required a filename to be passed in
    #if len(sys.argv) < 2:
    #    print("Error. Need handin list filename.")
    #    exit(1)
    #subs = sys.argv[1]
    #subs_file = open(subs)

    # new version just reads from stdin
    subs_file = sys.stdin
    lines = subs_file.readlines()
    lines = [line for line in lines if "not find project" not in line and "No submission" not in line]

    tas = ["Chenhao", "Kaiwei", "Robert", "Guanzhou", "Saurabh"]
    #tas = ["TA1", "TA2", "TA3", "TA4", "TA5"]

    fair_share = int(len(lines)/len(tas))

    # deal with the remainder
    unaccounted = len(lines) - (fair_share * len(tas))
    extra = {}
    for ta in tas:
        # by default, each TA will have to grade 0 extra
        extra[ta] = 0

    # draw names to see who will grade extra
    ta_bag = [ta for ta in tas]
    for i in range(unaccounted):
        drawn_name = random.choice(ta_bag)
        # each TA can only be drawn once
        ta_bag.remove(drawn_name)
        extra[drawn_name] = 1

    counter = 0
    for ta in tas:
      print("\n" + ta + ":\n")
      for i in range(fair_share + extra[ta]):
        print(str(counter + 1) + " " + lines[counter], end='')
        counter += 1

