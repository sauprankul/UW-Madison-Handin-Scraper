# UW-Madison-Handin-Scraper
This is a program built for the UW Madison CS Department. It looks at a specified "handin" directory and scrapes project submissions.
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

## roster.txt formatting;

An example roster.txt is included in the repo.

## Partner.txt formatting:

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


## Extra features:

- If a partner.txt contains "Firstname Lastname" instead of "Lastname, Firstname", the program will be able to handle it. Of course, "Firstname, Lastname" or "Lastname Firstname" are unacceptable.
- A roster.txt is not strictly necessary. If there is no roster, the script will rely on the partner.txts for name information, and, absent a well-formatted partner.txt, will use the csid (name of handin folder) as the name. The roster simply allows submissions with bad partner.txts to have a real name associated with them.
- The script can handle colon delimited identifiers such as "csid: skulkarni27". But it is neither necessary nor recommended. The order of the 3 fields is absolute.

## Known issues:
- This program does not distinguish between bad partner.txts and nonexistent partner.txts. This means that someone could put a bad partner.txt in their handin folder and get totally dropped from the final distribution. However, their partner (who has the code) will ideally also have a partner.txt and thus the grader will be able to manually match the two partners together at gradetime.

## Sample Output:
TA1:  
  
1 csid7 (csid7 has sub): Found code but BAD partner.txt. Check manually!  
2 csid9 (csid9 has sub): Found code but BAD partner.txt. Check manually!  
  
TA2:  
  
3 lname1,  fname1 (csid1 has sub), lname2,  fname2 (csid2): Good  
4 lname16, fname16 (csid16 doesn't have sub), lname17, fname17 (csid17): Partial match. Only found one partner.txt  
5 lname19, fname19 (csid19 doesn't have sub), lname18, fname18 (csid18): Partial match. Only found one partner.txt  
  
TA3:  
  
6 lname20, fname20 (csid20 has sub), lname21, fname21 (csid21): Partial match. Only found one partner.txt  
7 lname23, fname23 (csid23 doesn't have sub), lname22, fname22 (csid22): Partial match. Only found one partner.txt  
8 lname24, fname24 (csid24 has sub), lname25, fname25 (csid25): Good  
  
TA4:  
  
9 lname26, fname26 (csid26 has sub), lname27, fname27 (csid27): Good  
10 lname3, fname3 (csid3 has sub), lname4, fname4 (csid4): Found multiple submissions  
  
TA5:  
  
11 lname5, fname5 (csid5 has sub), lname6, fname6 (csid6): Partial match. Only found one partner.txt  
12 lname8, fname8 (csid8 has sub): Good  
