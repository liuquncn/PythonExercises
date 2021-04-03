
def prime_decompose(n):
    print n,
    print "=",
    if n<2:
         return
    i=2;
    while i*i<=n:
        while i*i<=n and n%i==0:
            print i,
            print "*",
            n=n/i
        i=i+1
    print n

if __name__=="__main__":
    prime_decompose(2**100-1)
    prime_decompose(149)

#bug report: 
#  prime_decompose(2**100-3) works fine.
#  prime_decompose(2**100-3) will print: "1267650600228229401496703205373 = 13 * 419 *" then the engine will crash