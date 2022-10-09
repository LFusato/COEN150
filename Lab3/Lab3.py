import math

primeTable = list()
#given values
e = 431
n = 9047783
cipherText = [7677954, 2327391, 2547721, 7062158, 2499758, 8238141, 8813209, 4428027, 6456849, 8238141, 2327391, 4565592, 7933833, 365998, 6957367, 6169593, 2811371]

#function that finds p and q given n, calcuates phi_n
def findPrimes():
    primeList = open("RSALabPrimes.txt", "r")
    #loop through file storing numbers in table
    for x in primeList:
        primeTable.append(int(x))

    pIndex = 0

    #loop through table twice, multipling each possible number combination
    while pIndex < len(primeTable):
        qIndex = 0
        while qIndex < len(primeTable):
            p = primeTable[pIndex]
            q = primeTable[qIndex]

            guessN = p * q
            #if the multiplied numbers are equal to n, that is the p and q
            if guessN == n:
                print("p is " + str(p) + " and q is " + str(q))
                phiN = (p-1) * (q-1)
                primeList.close()
                return phiN
            qIndex += 1
        pIndex += 1

#function that finds d based on phi_n and e
def findE(phiN):
    print("PhiN is " + str(phiN))
    (A1, A2, A3) = (1, 0, phiN)
    (B1, B2, B3) = (0, 1, e)

    #loops continuously until d is found
    #follows math found in lab instructions
    while True:
        if B3 == 0:
            print("A3 is " + str(A3))
            return A3
        if B3 == 1:
            print("B3 is " + str(B3) + " with inverse " + str(B2))
            return B2
        Q = math.floor(A3/B3)
        (T1, T2, T3) = (A1 - (Q * B1), A2 - (Q * B2), A3 - (Q * B3))
        (A1, A2, A3) = (B1, B2, B3)
        (B1, B2, B3) = (T1, T2, T3)

#function that decrypts message
def decryptMessage(d):
    print("The decryption for the message is:", end = ' ')
    #for each encrypted value, puts to power of d and mods by n
    for x in cipherText:
        message = pow(x,d,n)
        #prints result to one line
        print(chr(message), end = '')
    print(" ")
        

phiN = findPrimes()
d = findE(phiN)
decryptMessage(d)
