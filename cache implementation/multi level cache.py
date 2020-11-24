import math
import queue
import sys

from tabulate import tabulate
global s
global c
global b
global n
global tag1
global tag2
global linenumbit1
global linenumbit2
global bool
global cacheDirect1
global cacheDirect2
global calc1
global calc2
global cacheAssociative1
global cacheAssociative2
global NWayAssociative1
global NWayAssociative2
global quea1
global quea2
global Nque1
global Nque2
global tagS1
global tagS2

print("S will be equal to no. of line * No. of block * Size of 1 block(32 bit in this case)")
while True:


    try:
        c = int(input("No. of cache lines:"))
        if c > 0:
            break

        else:
            print("Please enter positive integer ")
    except ValueError:
        print("Please enter integer ")
while True:
    try:
        b = int(input("Block size :"))
        if b > 0:
            break
        else:
            print("Please enter positive integer")
    except ValueError:
        print("Please enter integer ")
while True:
    try:
        n = int(input("N for n-way set associative memory"))
        if n > 0:
            break
        else:
            print("Please enter positive integer ")
    except ValueError:
        print("Please enter integer ")


s = c * b
cacheDirect1 = [ [None] * (b+3) for i in range(int(c/2)) ]
cacheDirect2 = [ [None] * (b+3) for i in range(c) ]

quea1= queue.Queue(maxsize=int(c/2))
quea2= queue.Queue(maxsize=c)

cacheAssociative1 = [ [None] * (b+3) for i in range(int(c/2)) ]
cacheAssociative2 = [ [None] * (b+3) for i in range(c) ]

calc1=0
calc2=0

NWayAssociative1 = [ [None] * (b+3) for i in range(int(c/2)) ]
NWayAssociative2 = [ [None] * (b+3) for i in range(c) ]

linenumbit1 =int(math.log(c/2,2))
linenumbit2 =linenumbit1 +1
blockbit =int(math.log(b,2))

numberOfSet1= math.ceil(c/(2*n))
numberOfSet2= math.ceil(c/n)



if numberOfSet1==1:
    numberOfSetBit1=1
else:
    numberOfSetBit1= math.ceil((math.log(numberOfSet1,2)))

if numberOfSet2==1:
    numberOfSetBit2=1
else:
    numberOfSetBit2= math.ceil((math.log(numberOfSet2,2)))


tag1= 32- linenumbit1 - blockbit
tag2= 32- linenumbit2 - blockbit


tagS1= 32 - numberOfSetBit1 - blockbit
tagS2= 32 - numberOfSetBit2 - blockbit

Nque1=[]
for i in range(0,numberOfSet1):
    Nque1.append([])

Nque2=[]
for i in range(0,numberOfSet2):
    Nque2.append([])


def check_bin(value):
    value=set(value)
    temp = {'0','1'}

    if temp == value or value =={'1'} or value =={'0'}:
        return True
    else:
        return False
def check():
    if math.modf( math.log(c,2))[0]!=0:
        print("Number of cache lines must be in power of 2")
        return False
    if math.modf( math.log(b,2))[0]!=0:
        print("Block size must be in power of 2")
        return False

    if n<1 and n>int(c/2):
        print("N must lie between 1 and Cl/2")
        return False

    if c<2 or b <2:
        print("All value must be greater than or equal to 2")
        return False

    if s/b==c:
        return True
    else:
        return False
bool = check()
def checkinput(input):

    if check_bin(input):
        pass
    else:
        print("Address must be in Binary")
        return False

    if len(input)!=32:

        print("Address must 32 bit,")
        return False
    return True
def linenum1(num):
    num=num[tag1:tag1+linenumbit1]
    num = "0b" + num
    return int(num, 2)
def linenum2(num):
    num=num[tag2:tag2+linenumbit2]
    num = "0b" + num
    return int(num, 2)
def blocknum1(num):
    num=num[tag1+linenumbit1:]
    num = "0b" + num
    return int(num, 2)
def blocknum2(num):
    num=num[tag2+linenumbit2:]
    num = "0b" + num
    return int(num, 2)
def directMappingR(address):

    linenumber1 = linenum1(address)
    linenumber2 = linenum2(address)

    if cacheDirect1[linenumber1][b+2]==None:
        if cacheDirect2[linenumber2][b+2]==None:

            cacheDirect1[linenumber1][b+2]=address
            cacheDirect1[linenumber1][1] = address[tag1:tag1+linenumbit1]
            for i in range(b):
                cacheDirect1[linenumber1][i+2] = None
            cacheDirect1[linenumber1][0] = address[:tag1]

            cacheDirect2[linenumber2][b + 2] = address
            for i in range(b):
                cacheDirect2[linenumber2][i+2] = None
            cacheDirect2[linenumber2][1] = address[tag2:tag2 + linenumbit2]
            cacheDirect2[linenumber2][0] = address[:tag2]

            print('"Address not found at level 1 and 2 both" ')

        elif cacheDirect2[linenumber2][b+2]==address:
            cacheDirect1[linenumber1][b + 2] = address
            for i in range(b):
                cacheDirect1[linenumber1][i+2] = None
            cacheDirect1[linenumber1][1] = address[tag1:tag1 + linenumbit1]
            cacheDirect1[linenumber1][0] = address[:tag1]


    else:
        if  cacheDirect1[linenumber1][b+2]==address:
            for i in range(b):
                cacheDirect2[linenumber2][i + 2] = None
                for i in range(b):
                    cacheDirect1[linenumber1][i + 2] = None
                print("Hit at level 1" )
        else:
            if cacheDirect2[linenumber2][b + 2] == address:
                print("Hit at level 2")
                cacheDirect1[linenumber1][b + 2] = address
                for i in range(b):
                    cacheDirect1[linenumber1][i + 2] = None

                cacheDirect1[linenumber1][1] = address[tag1:tag1 + linenumbit1]
                cacheDirect1[linenumber1][0] = address[:tag1]


            else:
                print("Current data is replaced by data at " + address)

                cacheDirect1[linenumber1][b+2] = address
                for i in range(b):
                    cacheDirect1[linenumber1][i + 2] = None

                cacheDirect1[linenumber1][1] = address[tag1:tag1 + linenumbit1]
                cacheDirect1[linenumber1][0] = address[:tag1]
                cacheDirect2[linenumber2][b + 2] = address
                for i in range(b):
                    cacheDirect2[linenumber2][i + 2] = None

                cacheDirect2[linenumber2][1] = address[tag2:tag2 + linenumbit2]
                cacheDirect2[linenumber2][0] = address[:tag2]
def search (arr,input):
    for i in range(len(arr)):

        if arr[i][b+2]==input:

            return i
    return -1
def associativeMappingR(address):
    global quea1
    global quea2
    global calc1
    global calc2
    if calc1==0:

        print('"Address not found " ')
        cacheAssociative1[calc1][b+2]= address
        for i in range(b):
            cacheAssociative1[calc1][i + 2] = None

        cacheAssociative1[calc1][1] = address[tag1:tag1 + linenumbit1]
        cacheAssociative1[calc1][0] = address[:tag1]
        quea1.put(calc1)
        calc1=calc1+1


        cacheAssociative2[calc2][b + 2] = address
        for i in range(b):
            cacheAssociative2[calc2][i + 2] = None
        cacheAssociative2[calc2][1] = address[tag2:tag2 + linenumbit2]
        cacheAssociative2[calc2][0] = address[:tag2]
        quea2.put(calc2)
        calc2 = calc2 + 1

    elif calc2<int(c):
        if calc1<int(c/2):

            if search(cacheAssociative1,address) > -1:
                for i in range(b):
                    cacheAssociative1[search(cacheAssociative1,address)][i + 2] = None
                for i in range(b):
                    cacheAssociative2[search(cacheAssociative2, address)][i + 2] = None

                print("Hit at cache 1")

            else:
                if search(cacheAssociative2, address) > -1:
                    print("Hit at cache 2")
                    for i in range(b):
                        cacheAssociative2[search(cacheAssociative2, address)][i + 2] = None

                    cacheAssociative1[calc1][b + 2] = address
                    for i in range(b):
                        cacheAssociative1[calc1][i + 2] = None

                    cacheAssociative1[calc1][1] = address[tag1:tag1 + linenumbit1]
                    cacheAssociative1[calc1][0] = address[:tag1]
                    quea1.put(calc1)
                    calc = calc1 + 1
                else:

                    print('"Address not found "' )
                    cacheAssociative1[calc1][b+2]=address
                    for i in range(b):
                        cacheAssociative1[calc1][i + 2] = None
                    cacheAssociative1[calc1][1] = address[tag1:tag1 + linenumbit1]
                    cacheAssociative1[calc1][0] = address[:tag1]
                    quea1.put(calc1)
                    calc1 = calc1+1

                    cacheAssociative2[calc2][b + 2] = address
                    for i in range(b):
                        cacheAssociative2[calc2][i + 2] = None
                    cacheAssociative2[calc2][1] = address[tag2:tag2 + linenumbit2]
                    cacheAssociative2[calc2][0] = address[:tag2]
                    quea2.put(calc2)
                    calc2 = calc2 + 1
        else:
            if search(cacheAssociative1,address) > -1:
                print("Hit at cache 1")
            else:
                if search(cacheAssociative2, address) > -1:
                    print("Hit at cache 2")
                    temp = quea1.get()
                    cacheAssociative1[temp][b + 2] = address

                    for i in range(b):
                        cacheAssociative1[temp][i + 2] = None
                    cacheAssociative1[temp][1] = address[tag1:tag1 + linenumbit1]
                    cacheAssociative1[temp][0] = address[:tag1]
                    quea1.put(temp)
                else:
                    temp1 = quea1.get()
                    cacheAssociative1[temp1][b + 2] = address
                    for i in range(b):
                        cacheAssociative1[temp1][i + 2] = None
                    cacheAssociative1[temp1][1] = address[tag1:tag1 + linenumbit1]
                    cacheAssociative1[temp1][0] = address[:tag1]
                    print("Current data is replaced by data at " + address)
                    quea1.put(temp1)

                    cacheAssociative2[calc2][b + 2] = address
                    for i in range(b):
                        cacheAssociative2[calc2][i + 2] = None
                    cacheAssociative2[calc2][1] = address[tag2:tag2 + linenumbit2]
                    cacheAssociative2[calc2][0] = address[:tag2]
                    quea2.put(calc2)
                    calc2 = calc2 + 1






    else:
        if search(cacheAssociative1,address) >-1:
            print("Hit at level 1" )
        else:
            if search(cacheAssociative2,address) >-1:
                print("Hit at level 2")
                temp = quea1.get()
                cacheAssociative1[temp][b + 2] = address
                for i in range(b):
                    cacheAssociative1[temp][i + 2] = None
                cacheAssociative1[temp][1] = address[tag1:tag1 + linenumbit1]
                cacheAssociative1[temp][0] = address[:tag1]
                quea1.put(temp)
            else:

                temp1 = quea1.get()
                cacheAssociative1[temp1][b+2] = address
                for i in range(b):
                    cacheAssociative1[temp1][i + 2] = None
                cacheAssociative1[temp1][1] = address[tag1:tag1 + linenumbit1]
                cacheAssociative1[temp1][0] = address[:tag1]
                print("Current data is replaced by data at " + address )
                quea1.put(temp1)

                temp2 = quea2.get()
                for i in range(b):
                    cacheAssociative2[temp2][i + 2] = None
                cacheAssociative2[temp2][b + 2] = address
                cacheAssociative2[temp2][1] = address[tag2:tag2 + linenumbit2]
                cacheAssociative2[temp2][0] = address[:tag2]
                print("Current data is replaced by data at " + address)
                quea2.put(temp2)
def searchNway1(address,setnum):
    if n>c/2:
        for i in range(0, setnum(n+1)):
            if NWayAssociative1[i][b + 2] == address:
                return i


    else:
        for i in range(n*setnum, setnum*n+n):
            if NWayAssociative1[i][b+2]==address:

                return i
    return -1
def searchNway2(address,setnum):

    for i in range(setnum*n,(setnum+1)*n):

        if NWayAssociative2[i][b+2]==address:
            return i
    return -1
def getSetNumber1(string):
    if c==n:
        return 0
    string = string[tagS1:tagS1+numberOfSetBit1]

    string= "0b"+string
    return int(string,2)
def getSetNumber2(string):
    if n==c:
        return 0
    string = string[tagS2:tagS2+numberOfSetBit2]
    string= "0b"+string
    return int(string,2)
def NWaySetAssociativeMappingR(address):

    setnum1 = getSetNumber1(address)
    setnum2 = getSetNumber2(address)


    lineNumber1 =searchNway1(address,setnum1)
    lineNumber2 =searchNway2(address,setnum2)


    if lineNumber1==-1:

        if lineNumber2==-1:
            if n==c:
                buggy=n/2

            else:
                buggy=n
            if len(Nque1[setnum1])==buggy:
                NWayAssociative1[Nque1[setnum1][0]][b+2] = address
                for i in range(b):
                    NWayAssociative1[Nque1[setnum1][0]][i + 2] = None
                NWayAssociative1[Nque1[setnum1][0]][1] = address[tagS1:tagS1 + numberOfSetBit1]
                NWayAssociative1[Nque1[setnum1][0]][0] = address[:tagS1]
                if n== c:
                    NWayAssociative1[Nque1[setnum1][0]][1] = "0"

                Nque1[setnum1].append(Nque1[setnum1][0])
                print("Current data is replaced by data at " + address + " (Cache number 1 )")
                del Nque1[setnum1][0]
            else:
                NWayAssociative1[setnum1*n + len(Nque1[setnum1])][b + 2] = address
                for i in range(b):
                    NWayAssociative1[setnum1*n + len(Nque1[setnum1])][i + 2] = None
                NWayAssociative1[setnum1*n + len(Nque1[setnum1])][1] = address[tagS1:tagS1 + numberOfSetBit1]
                NWayAssociative1[setnum1*n + len(Nque1[setnum1])][0] = address[:tagS1]
                if n == c:
                    NWayAssociative1[setnum1*n + len(Nque1[setnum1])][1] = "0"

                Nque1[setnum1].append(setnum1*n + len(Nque1[setnum1]))
                print('"Address not found "'+ " (Cache number 1 )")

            if len(Nque2[setnum2])==n:
                NWayAssociative2[Nque2[setnum2][0]][b+2] = address
                for i in range(b):
                    NWayAssociative2[Nque2[setnum2][0]][i + 2] = None
                NWayAssociative2[Nque2[setnum2][0]][1] = address[tagS2:tagS2 + numberOfSetBit2]
                NWayAssociative2[Nque2[setnum2][0]][0] = address[:tagS2]
                if n == c:
                    NWayAssociative2[Nque2[setnum2][0]][1] = "0"
                Nque2[setnum2].append(Nque2[setnum2][0])
                print("Current data is replaced by data at " + address + " (Cache number 2 )")
                del Nque2[setnum2][0]
            else:
                for i in range(b):
                    NWayAssociative2[setnum2*n + len(Nque2[setnum2])][i + 2] = None
                NWayAssociative2[setnum2*n + len(Nque2[setnum2])][b + 2] = address
                NWayAssociative2[setnum2*n + len(Nque2[setnum2])][1] = address[tagS2:tagS2 + numberOfSetBit2]
                NWayAssociative2[setnum2*n + len(Nque2[setnum2])][0] = address[:tagS2]
                if n == c:
                    NWayAssociative2[setnum2*n + len(Nque2[setnum2])][1] = "0"
                Nque2[setnum2].append(setnum2*n + len(Nque2[setnum2]))
                print('"Address not found "'+ " (Cache number 2 )")


        else:
            if len(Nque1[setnum1])==n:
                NWayAssociative1[Nque1[setnum1][0]][b+2] = address

                for i in range(b):
                    NWayAssociative1[Nque1[setnum1][0]][i + 2] = None
                NWayAssociative1[Nque1[setnum1][0]][1] = address[tagS1:tagS1 + numberOfSetBit1]
                NWayAssociative1[Nque1[setnum1][0]][0] = address[:tagS1]
                if n == c:
                    NWayAssociative1[Nque1[setnum1]][1] = "0"
                Nque1[setnum1].append(Nque1[setnum1][0])
                del Nque1[setnum1][0]
            else:
                for i in range(b):
                    NWayAssociative1[setnum1*n + len(Nque1[setnum1])][i + 2] = None
                NWayAssociative1[setnum1*n + len(Nque1[setnum1])][b + 2] = address
                NWayAssociative1[setnum1*n + len(Nque1[setnum1])][1] = address[tagS1:tagS1 + numberOfSetBit1]
                NWayAssociative1[setnum1*n + len(Nque1[setnum1])][0] = address[:tagS1]
                if n == c:
                    NWayAssociative1[setnum1*n + len(Nque1[setnum1])][1] = "0"
                Nque1[setnum1].append(setnum1*n + len(Nque1[setnum1]))

            print("Hit at cache 2")


    else:
        for i in range(b):
            NWayAssociative1[Nque1[setnum1][0]][i + 2] = None

        for i in range(b):
            NWayAssociative2[Nque2[setnum2][0]][i + 2] = None

        print('Hit at cache 1')
def directMappingW(address,data):

    linenumber1 = linenum1(address)
    linenumber2 = linenum2(address)
    cacheDirect1[linenumber1][blocknum1(address) + 2] = data
    cacheDirect1[linenumber1][b + 2] = address
    cacheDirect1[linenumber1][1] = address[tag1:tag1 + linenumbit1]
    cacheDirect1[linenumber1][0] = address[:tag1]

    cacheDirect2[linenumber2][blocknum2(address) + 2] = data
    cacheDirect2[linenumber2][b + 2] = address
    cacheDirect2[linenumber2][1] = address[tag2:tag2 + linenumbit2]
    cacheDirect2[linenumber2][0] = address[:tag2]
def associativeMappingW(address,data):
    global calc1
    global calc2
    location1 = search(cacheAssociative1,address)
    location2 = search(cacheAssociative2,address)
    if location1>-1:
        cacheAssociative1[location1][blocknum1(address)+2]=data
        cacheAssociative2[location2][blocknum2(address)+2]=data
    else:
        if location2>-1:
            cacheAssociative2[location2][blocknum2(address)+2]=data
            temp = quea1.get()
            cacheAssociative1[temp][blocknum1(address) + 2] = data
            cacheAssociative1[temp][b + 2] = address
            cacheAssociative1[temp][1] = address[tag1:tag1 + linenumbit1]
            cacheAssociative1[temp][0] = address[:tag1]
            quea1.put(temp)
        else:
            if quea1.empty()==True:
                temp=0
                calc1=calc1+1
                calc2=calc2+1
            else:
                temp = quea1.get()
            tempadd=cacheAssociative1[temp][b+2]
            cacheAssociative1[temp][blocknum1(address) + 2] = data
            cacheAssociative1[temp][b + 2] = address
            cacheAssociative1[temp][1] = address[tag1:tag1 + linenumbit1]
            cacheAssociative1[temp][0] = address[:tag1]
            quea1.put(temp)
            p=search(cacheAssociative2,tempadd)
            cacheAssociative2[p][blocknum1(address) + 2] = data
            cacheAssociative2[p][b + 2] = address
            cacheAssociative2[p][1] = address[tag2:tag2 + linenumbit2]
            cacheAssociative2[p][0] = address[:tag2]
            quea2.put("hello")
            while True:
                a=quea2.get()
                if a=="hello":
                    break
                if a==p:
                    pass
                else:
                    quea2.put(a)
            quea2.put(temp)
def blocknumA1(num):
    num = num[tagS1+numberOfSetBit1:]
    num = "0b" + num
    return int(num, 2)
def blocknumA2(num):
    num = num[tagS2+numberOfSetBit2:]
    num = "0b" + num
    return int(num, 2)
def NWaySetAssociativeMappingW(address,data):
    setnum1 = getSetNumber1(address)
    setnum2 = getSetNumber2(address)

    location1 = searchNway1(address, setnum1)
    location2 = searchNway2(address, setnum2)

    if location1>-1:
        NWayAssociative1[location1][blocknumA1(address)+2]=data
        NWayAssociative2[location2][blocknumA2(address)+2]=data
    else:
        if location2>-1:
            NWayAssociative2[location2][blocknumA2(address)+2]=data
            NWayAssociative1[Nque1[setnum1][0]][b + 2] = address
            NWayAssociative1[Nque1[setnum1][0]][blocknumA1(address)] = data
            NWayAssociative1[Nque1[setnum1][0]][1] = address[tagS1:tagS1 + numberOfSetBit1]
            NWayAssociative1[Nque1[setnum1][0]][0] = address[:tagS1]
            if n == c:
                NWayAssociative1[Nque1[setnum1]][1] = "0"
            Nque1[setnum1].append(Nque1[setnum1][0])
            Nque1[setnum1].append(Nque1[setnum1][0])
            del Nque1[setnum1][0]
        else:
            if len(Nque1[setnum1])==0:
                Nque1[setnum1].append(setnum1*n)
                Nque2[setnum2].append(setnum2*n)

            NWayAssociative1[Nque1[setnum1][0]][b + 2] = address
            NWayAssociative1[Nque1[setnum1][0]][blocknumA1(address)+2] = data
            NWayAssociative1[Nque1[setnum1][0]][1] = address[tagS1:tagS1 + numberOfSetBit1]
            NWayAssociative1[Nque1[setnum1][0]][0] = address[:tagS1]
            if n == c:
                NWayAssociative1[Nque1[setnum1]][1] = "0"
            Nque1[setnum1].append(Nque1[setnum1][0])
            Nque1[setnum1].append(Nque1[setnum1][0])
            del Nque1[setnum1][0]


            NWayAssociative2[Nque2[setnum2][0]][b + 2] = address
            NWayAssociative2[Nque2[setnum2][0]][blocknumA2(address)+2] = data
            NWayAssociative2[Nque2[setnum2][0]][1] = address[tagS2:tagS2 + numberOfSetBit2]
            NWayAssociative2[Nque2[setnum2][0]][0] = address[:tagS2]
            if n == c:
                NWayAssociative2[Nque2[setnum2]][1] = "0"
            Nque2[setnum2].append(Nque2[setnum2][0])
            Nque2[setnum2].append(Nque2[setnum2][0])
            del Nque2[setnum2][0]
            if len(Nque1[setnum1])==0:
                Nque1[setnum1].append(0)
                Nque2[setnum2].append(0)

while bool:
    print()
    print("Type 1 to read ")
    print("Type 2 to write ")
    print("Type 3 to print Caches")
    print("Type 4 to exit ")
    print()

    try:
        command = input()
        if command == "":
            command=0
        else:
            command=int(command)
        if command>0 and command<5:
            pass
        else:
            print("Please enter integer betweem 1 and 4")
    except ValueError and NameError:
        print("Please enter integer betweem 1 and 4")



    if command==4:
        print("Thanks You")
        break


    if command==3:
        header1= ["Tag", "Line number"]
        for i in range(b):
            header1.append("W"+str(i))

        CD = cacheDirect1.copy()
        CD2 = cacheDirect2.copy()
        for i in range(int(c/2)):
            CD[i]=CD[i][:-1]
        for i in range(c):
            CD2[i]=CD2[i][:-1]
        print("Direct Mapping:")
        print()
        print("Cache level 1")
        print()
        print(tabulate(CD,headers=header1, tablefmt="grid", showindex="always"  ))
        print()
        print("Cache level 2")
        print()
        print(tabulate(CD2, headers=header1, tablefmt="grid", showindex="always"))
        print()




        print("Associative Mapping:")
        CA = cacheAssociative1.copy()
        CA2 = cacheAssociative2.copy()
        for i in range(int(c/2)):
            CA[i] = CA[i][:-1]
        print()
        for i in range(c):
            CA2[i] = CA2[i][:-1]
        print("Cache level 1")
        print()
        print(tabulate(CA, headers=header1, tablefmt="grid", showindex="always"))
        print()
        print("Cache level 2")
        print()
        print(tabulate(CA2, headers=header1, tablefmt="grid", showindex="always"))
        print()


        print("N- Way set Associative Mapping:")
        print()
        header2 = ["Tag", " Set number"]
        for i in range(b):
            header2.append("W" + str(i))
        CN = NWayAssociative1.copy()
        for i in range(int(c/2)):
            CN[i] = CN[i][:-1]
        CN2 = NWayAssociative2.copy()
        for i in range(c):
            CN2[i] = CN2[i][:-1]
        print("Cache level 1")
        print()
        print(tabulate(CN, headers=header2, tablefmt="grid", showindex="always"))
        print()
        print("Cache level 2")
        print()
        print(tabulate(CN2, headers=header2, tablefmt="grid", showindex="always"))
        print()

    if command==1:
        address = input("Address:")
        if checkinput(address)==False:
            pass
        else:
            print("Direct mapping")
            directMappingR(address)
            print("Associative Mapping:")
            associativeMappingR(address)
            print("N- Way set Associative Mapping:")
            NWaySetAssociativeMappingR(address)

    if command==2:

        address = input("Address:")
        if checkinput(address)==False:
            pass
        else:
            data = input("Data:")
            if sys.getsizeof(data)>35:
                print("Data should be under word limit i.e. 32 bit")
            else:
                directMappingW(address,data)

                associativeMappingW(address,data)
                NWaySetAssociativeMappingW(address,data)

    command=0