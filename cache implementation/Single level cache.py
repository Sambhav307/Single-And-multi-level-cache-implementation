import math
import queue
import sys
from tabulate import tabulate
global s
global c
global b
global tag
global linenumbit
global bool
global cacheDirect
global calc
global cacheAssociative
global n
global NWayAssociative
global quea
global Nque
global tagS
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
cacheDirect = [ [None] * (b+3) for i in range(c) ]
quea= queue.Queue(maxsize=c)
cacheAssociative = [ [None] * (b+3) for i in range(c) ]
NWayAssociative = [ [None] * (b+3) for i in range(c) ]


calc=0
linenumbit =int(math.log(c,2))
blockbit =int(math.log(b,2))
numberOfSet= math.ceil(c/n)
if numberOfSet==1:
    numberOfSetBit=1
else:
    numberOfSetBit= math.ceil((math.log(numberOfSet,2)))
tag= 32- linenumbit- blockbit
tagS= 32 - numberOfSetBit -  blockbit
Nque=[]
for i in range(0,numberOfSet):
    Nque.append([])

def check_bin(value):
    value=set(value)
    temp = {'0','1'}

    if temp == value or value =={'1'} or value =={'0'}:
        return True
    else:
        return False
def check():

    if math.modf( math.log(c,2))[0]!=0:
        print(" Number of cache lines must be in power of 2 ")
        return False
    if math.modf( math.log(b,2))[0]!=0:
        print(" Block size must be in power of 2 ")
        return False

    if n<1 and n>c:
        print(" N must lie between 1 and Cl ")
        return False

    if c<2 or b <2:
        print(" CL and B must be greater than or equal to 2 ")
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
        print(" Address must be in Binary ")
        return False

    if len(input)!=32:

        print("Address must 32 bit ")
        return False
    return True
def linenum(num):
    num=num[tag:tag+linenumbit]
    num = "0b" + num
    return int(num, 2)
def blocknum(num):
    num=num[tag+linenumbit:]
    num = "0b" + num
    return int(num, 2)
def directMappingR(address):

    linenumber = linenum(address)

    if cacheDirect[linenumber][b+2]==None:
        cacheDirect[linenumber][b+2]=address
        for i in range(b):
            cacheDirect[linenumber][i + 2] = None
        cacheDirect[linenumber][1] = address[tag:tag+linenumbit]
        cacheDirect[linenumber][0] = address[:tag]
        print('"Address not found " ')
    else:
        if  cacheDirect[linenumber][b+2]==address:
            for i in range(b):
                cacheDirect[linenumber][i + 2] = None
            print(" Hit " )
        else:
            for i in range(b):
                cacheDirect[linenumber][i + 2] = None
            cacheDirect[linenumber][b+2] = address
            cacheDirect[linenumber][1] = address[tag:tag + linenumbit]
            cacheDirect[linenumber][0] = address[:tag]
            print("Current data is replaced by data at " + address)
def search (arr,input):
    for i in range(c):

        if arr[i][b+2]==input:

            return i
    return -1
def associativeMappingR(address):
    global quea
    global calc
    if calc==0:

        print('"Address not found " ')
        cacheAssociative[calc][b+2]= address
        for i in range(b):
            cacheAssociative[calc][i + 2] = None
        cacheAssociative[calc][1] = address[tag:tag + linenumbit]
        cacheAssociative[calc][0] = address[:tag]
        quea.put(calc)
        calc=calc+1
    elif calc<c:
        if search(cacheAssociative,address) > -1:
            for i in range(b):
                cacheAssociative[search(cacheAssociative,address)][i + 2] = None
            print("Hit")

        else:
            print('"Address not found "' )
            for i in range(b):
                cacheAssociative[calc][i + 2] = None
            cacheAssociative[calc][b+2]=address
            cacheAssociative[calc][1] = address[tag:tag + linenumbit]
            cacheAssociative[calc][0] = address[:tag]
            quea.put(calc)
            calc=calc+1

    else:
        if search(cacheAssociative,address) >-1:
            for i in range(b):
                cacheAssociative[search(cacheAssociative,address)][i + 2] = None
            print("Hit" )
        else:
            temp = quea.get()
            for i in range(b):
                cacheAssociative[temp][i + 2] = None
            cacheAssociative[temp][b+2] = address
            cacheAssociative[temp][1] = address[tag:tag + linenumbit]
            cacheAssociative[temp][0] = address[:tag]
            print("Current data is replaced by data at " + address )
            quea.put(temp)
def associativeMappingW(addrress,data):
    global quea
    global calc
    if calc==0:
        cacheAssociative[calc][b+2]= address
        cacheAssociative[calc][1] = address[tag:tag + linenumbit]
        cacheAssociative[calc][0] = address[:tag]
        cacheAssociative[calc][blocknum(address)+2]=data
        quea.put(calc)
        calc=calc+1
    elif calc<c:
        tempsearch=search(cacheAssociative,address)
        if  tempsearch>= 0:
            cacheAssociative[tempsearch][blocknum(address) + 2] = data

        else:
            cacheAssociative[calc][blocknum(address) + 2] = data
            cacheAssociative[calc][b+2]=address
            cacheAssociative[calc][1] = address[tag:tag + linenumbit]
            cacheAssociative[calc][0] = address[:tag]
            quea.put(calc)
            calc=calc+1

    else:
        tempsearch = search(cacheAssociative, address)
        if tempsearch >= 0:
            cacheAssociative[tempsearch][blocknum(address) + 2] = data

        else:
            temp = quea.get()
            cacheAssociative[temp][blocknum(address) + 2] = data
            cacheAssociative[temp][b+2] = address
            cacheAssociative[temp][1] = address[tag:tag + linenumbit]
            cacheAssociative[temp][0] = address[:tag]
            quea.put(temp)
def searchNway(address,setnum):

    for i in range(setnum,setnum+n):
        if NWayAssociative[i][b+2]==address:
            return i
    return -1
def getSetNumber(string):
    if n==c:
        return 0
    string = string[tagS:tagS+numberOfSetBit]

    string= "0b"+string
    return int(string,2)
def NWaySetAssociativeMappingR(address):


    setnum = getSetNumber(address)


    lineNumber =searchNway(address,setnum)
    if lineNumber==-1:

        if len(Nque[setnum])==n:
            NWayAssociative[Nque[setnum][0]][b+2] = address
            for i in range(b):
                NWayAssociative[Nque[setnum][0]][i + 2] = None
            NWayAssociative[Nque[setnum][0]][1] = address[tagS:tagS + numberOfSetBit]
            NWayAssociative[Nque[setnum][0]][0] = address[:tagS]
            if n == c:
                NWayAssociative[Nque[setnum][0]][1] = "0"
            Nque[setnum].append(Nque[setnum][0])
            print("Current data is replaced by data at " + address)
            del Nque[setnum][0]
        else:
            for i in range(b):
                NWayAssociative[setnum*n + len(Nque[setnum])][i + 2] = None
            NWayAssociative[setnum*n + len(Nque[setnum])][b + 2] = address
            NWayAssociative[setnum*n + len(Nque[setnum])][1] = address[tagS:tagS + numberOfSetBit]
            NWayAssociative[setnum*n + len(Nque[setnum])][0] = address[:tagS]
            if n==c:
                NWayAssociative[setnum*n + len(Nque[setnum])][1] = "0"
            Nque[setnum].append(setnum*n + len(Nque[setnum]))
            print('"Address not found " ')


    else:
        for i in range(b):
            NWayAssociative[Nque[setnum][0]][i + 2] = None

        print('Hit')
def blocknumA(num):
    num = num[tagS+numberOfSetBit:]
    num = "0b" + num
    return int(num, 2)
def NWaySetAssociativeMappingW(address,data):


    setnum = getSetNumber(address)

    lineNumber =searchNway(address,setnum)
    if lineNumber==-1:
        if len(Nque[setnum])==n:

            NWayAssociative[Nque[setnum][0]][b+2] = address
            NWayAssociative[Nque[setnum][0]][blocknumA(address)+2] = data
            NWayAssociative[Nque[setnum][0]][1] = address[tagS:tagS + numberOfSetBit]
            NWayAssociative[Nque[setnum][0]][0] = address[:tagS]
            if n == c:
                NWayAssociative[Nque[setnum][0]][1] = "0"
            Nque[setnum].append(Nque[setnum][0])
            del Nque[setnum][0]


        else:

            NWayAssociative[setnum*n + len(Nque[setnum])][blocknumA(address) + 2] = data
            NWayAssociative[setnum*n + len(Nque[setnum])][b + 2] = address
            NWayAssociative[setnum*n+ len(Nque[setnum])][1] = address[tagS:tagS + numberOfSetBit]
            NWayAssociative[setnum*n + len(Nque[setnum])][0] = address[:tagS]
            if n==c:
                NWayAssociative[setnum*n + len(Nque[setnum])][1] = "0"
            Nque[setnum].append(setnum + len(Nque[setnum]))
            print('"Address not found " ')




    else:
        NWayAssociative[lineNumber][b + 2] = address
        NWayAssociative[lineNumber][blocknumA(address) + 2] = data
        NWayAssociative[lineNumber][1] = address[tagS:tagS + numberOfSetBit]
        NWayAssociative[lineNumber][0] = address[:tagS]
        print('Hit')
        if n==c:
            NWayAssociative[lineNumber][1] = "0"

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
            print(" Please enter integer between 1 and 4 ")
    except ValueError and NameError:
        print("Please enter integer between 1 and 4")

    if command==4:
        print("Thanks You")
        break
    if command==3:

        header1= ["Tag", "Line number"]
        for i in range(b):
            header1.append("W"+str(i))
        CD = cacheDirect.copy()
        for i in range(c):
            CD[i]=CD[i][:-1]
        print("Direct Mapping:")

        print(tabulate(CD,headers=header1, tablefmt="grid", showindex="always"  ))
        print()
        print("Associative Mapping:")
        CA = cacheAssociative.copy()
        for i in range(c):
            CA[i] = CA[i][:-1]

        print(tabulate(CA, headers=header1, tablefmt="grid", showindex="always"))
        print()


        print("N- Way set Associative Mapping:")



        header2 = ["Tag", " Set number"]
        for i in range(b):
            header2.append("W" + str(i))
        CN = NWayAssociative.copy()
        for i in range(c):
            CN[i] = CN[i][:-1]

        print(tabulate(CN, headers=header2, tablefmt="grid", showindex="always"))
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
                cacheDirect[linenum(address)][blocknum(address)+2]=data
                associativeMappingW(address,data)
                NWaySetAssociativeMappingW(address,data)
    command=0

sys.exit()
