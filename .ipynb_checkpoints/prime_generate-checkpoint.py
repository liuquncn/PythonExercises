
def prime_generate(n):
    prime_tag=[1]*(n+1);
    prime_tag[0]=prime_tag[1]=0;
    for i in range(2,n+1):
        if prime_tag[i]==1:
            for j in range(i+i,n+1,i):
                prime_tag[j]=0;
    for i in range(2,n+1):
        if prime_tag[i]==1:
            print i,

if __name__=='__main__':
    prime_generate(1000)
