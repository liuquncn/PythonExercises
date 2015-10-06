import string

srcfilename="2008041015031832.txt"
tgtfilename="2008041015031831.txt"

srcfile=open(srcfilename)
tgtfile=open(tgtfilename)

srcsent=[string.strip(x) for x in srcfile if len(string.strip(x))!=0]
tgtsent=[string.strip(x) for x in tgtfile if len(string.strip(x))!=0]

srclength=[len(x) for x in srcsent]
tgtlength=[len(x) for x in tgtsent]

