# UW-Madison-Handin-Scraper
This is a program built for the UW Madison CS Department. It looks at a specified "handin" directory and looks for project submissions.
It creates a list of submissions, pairs partners together using partner.txt files, filters out empty folders then distributes the submissions across the TAs named in distro.py.
This script was originally created by Saurabh Kulkarni (email: skulkarni27@wisc.edu) for Professor Barton Miller's FA20 CS537 class.

To use this script:

1) Log into a Linux CS Lab server
2) Clone this repo
3) Go into the UW-Madison-Handin-Scraper directory
4) Open driver.py and enter the correct handin directory.
5) If you have a roster, set the roster directory/filename.
6) Set the TA names in distro.py if necessary.
7) Run ```python3 driver.py <projname> | python3 distro.py```


After cloning, you can test the program by running ```python3 driver.py proj2 | python3 distro.py```. The expected output is in ```expected.txt``` inside the provided ```handin/``` test folder.

roster.txt formatting;

An example roster.txt is included in the repo.

Partner.txt formatting:

An example partner.txt is included in the repo.

1) If you have a partner, only ONE of you should turn in code into the handin directory. The other should only have a partner.txt.

2) EVERYONE, including people who are working alone, must have a partner.txt. Especially the people who are turning code in for their duo.

3) The format of the partner.txt should be as follows

```
<Last Name>, <First Name>, <cs id>, <netid>
<Partner Last Name>, <Partner First Name>, <cs id>, <netid>
```

Example:
```
Kulkarni, Saurabh, skulkarni27, skulkarni27
Williams, Robert, rjava, rjwilliams22
```
It's fine to swap the order of the lines. You and your partner can have the same partner.txt.

Note the order and the comma separation. If you're working alone, your partner.txt will only have one line. This will allow us to confirm that you are indeed working alone and didn't just forget your partner.txt. Also, note that we're asking for Lastname, Firstname because Canvas gradebook entries are in lastname order.

Possible format errors:

- Swapping netID and CSID

- including campus ID rather than NetID. Your NetID is your wisc.edu email without "@wisc.edu".

- Including identifiers like "csid: <csid>". Only include the values.


Extra features:

- If a partner.txt contains "Firstname Lastname" instead of "Lastname, Firstname", the program will be able to handle it. Of course, "Firstname, Lastname" or "Lastname Firstname" are unacceptable.
- A roster.txt is not strictly necessary. If there is no roster, the script will rely on the partner.txts for name information, and, absent a well-formatted partner.txt, will use the csid (name of handin folder) as the name. The roster simply allows submissions with bad partner.txts to have a real name associated with them.
- The script can handle colon delimited identifiers such as "csid: skulkarni27". But it is neither necessary nor recommended. The order of the 3 fields is absolute.
