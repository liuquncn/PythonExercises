#coding=gbk

def substringtext(text,substringtable):

    class edgeset(dict): # a dict as nextword:set_of_ouside_edges
        def __init__(self):
            self.count=0

    graph={} # a dict as word:edgeset

    for (i,word) in enumerate(text): #print i,word
        if not graph.has_key(word): graph[word]=edgeset()
        outedgeset=graph[word]
        if i==len(text)-1:
            nextword=""
        else:
            nextword=text[i+1]
        if not outedgeset.has_key(nextword): outedgeset[nextword]=set();
        outedgeset[nextword].add(i)
        outedgeset.count+=1

    prefixtable={} # dict as startposition:set_of_inside_edges

    for (i,word) in enumerate(text):
        frequent=graph[word].count
        infrequent=0
        if i==len(text)-1 : outedgeset=set()
        else: outedgeset=graph[word][text[i+1]]
        for startposition in prefixtable.keys():
            infrequent=max(infrequent,len(prefixtable[startposition]))
            inedgeset=prefixtable[startposition]
            prefixtable[startposition]=set([inedge+1 for inedge in inedgeset])
            inedgeset=prefixtable[startposition]
            dupedgeset=inedgeset.intersection(outedgeset)
            if len(dupedgeset)<len(inedgeset): # add multi-word substring
                substring=tuple(text[startposition:i+1])
                if substringtable.has_key(substring):
                    substringtable[substring]+=1
                else:
                    substringtable[substring]=1
                prefixtable[startposition]=dupedgeset
            if len(prefixtable[startposition])==1:
                del prefixtable[startposition]
        if len(outedgeset)>max(1,infrequent):
            prefixtable[i]=outedgeset
        if len(graph[word])!=1 and frequent>infrequent: # add single-word substring
            substring=tuple(text[i:i+1])
            if substringtable.has_key(substring):
                substringtable[substring]+=1
            else:
                substringtable[substring]=1

def substring_from_file(inputfile,outputfile):

    text=[]
    for line in inputfile:
        for wordpos in line.split():
            splitpos=wordpos.find("/")
            if (splitpos==-1): word=wordpos
            else: word=wordpos[0:splitpos]
            text.append(word)
    inputfile.close()

    substringtable={}
    substringtext(text,substringtable)

    for (substring,freq) in sorted(substringtable.items(),key=lambda x:x[1],reverse = True):
        print >> outputfile, freq, ":",
        for word in substring:
             print >> outputfile, word,
        print >> outputfile

    outputfile.close()

def substring_from_string(inputstring):

    text=[]
    for wordpos in inputstring.split():
        splitpos=wordpos.find("/")
        if (splitpos==-1): word=wordpos
        else: word=wordpos[0:splitpos]
        text.append(word)

    substringtable={}
    substringtext(text,substringtable)

    for (substring,freq) in sorted(substringtable.items(),key=lambda x:x[1],reverse = True):
        print freq, ":",
        for word in substring:
             print word,
        print

if __name__ == "__main__":

    #inputfile=open("E:\\lang\\BookTechnical\\Python\\Test\\wordcount\\test(2M)_cla.txt","r")
    #outputfile=open("E:\\lang\\BookTechnical\\Python\\Test\\wordcount\\test(2M)_cla_result.txt","w")
    #inputfile=open("E:\\lang\\BookTechnical\\Python\\Test\\wordcount\\test.txt","r")
    #outputfile=open("E:\\lang\\BookTechnical\\Python\\Test\\wordcount\\test_result.txt","w")
    #substring_from_file(inputfile,outputfile)

    inputstring1 = "A B C D A B C D A B C D A B A C"
    inputstring2 = """
        各 省 、 区 、 市 和 经济特区
        全国 各省 、 区 、 市 的
        从 中央 到 省 、 区 、 地 、 市"""
    substring_from_string(inputstring2)
