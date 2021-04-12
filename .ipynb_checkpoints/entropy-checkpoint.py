from math import log

def entropy(list):
    sum=0
    for element in list: sum+=element
    en=0
    for element in list:
        probability=float(element)/float(sum)
        en-=probability*log(probability,2)
    return en

