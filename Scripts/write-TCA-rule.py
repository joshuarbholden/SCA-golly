# Implements Stranded Cellular Automata (first defined in https://archive.bridgesmathart.org/2016/bridges2016-127.html) in Golly.
#
# Rules/SCA-shared.rule should be in your personal rule directory.
# Scripts/write-SCA-rule.py takes a turning rule number and a crossing
# rule number, generates a Golly rule file in your personal rule
# directory, and then loads it up.
#
# contact:  holden@rose-hulman.edu



import golly as g

def statetocrosstrin (state):
    if len(state) < 2:
        return(1) #noncrossing
    elif state[1] = "L":
        return(0) #left on top
    elif state[1] = "R":
        return(2) #right on top
    else raise Exception("State not yet implemented")
    
def reflectstrand (strand):
    if strand == "R":
        return("L")
    elif strand == "L":
        return("R")
    else:
        return(strand)
        
        
def reflectstate (state):
    return(tuple(reversed(tuple(map(reflectstrand, state)))))
    

def setupruletable (crossingrule, turningrule):
    Rules = dict()
    bincrossrule = bin(crossingrule + 2^27)[-1:2:-1] #convert to binary in reverse
    binturnrule = bin(turningrule + 2^27)[-1:2:-1] #convert to binary in reverse
    states = [((),"e"),(("R",),"d"),(("L",),"d"),(("L","R"),"d"),(("R","L"),"d"),
                (("R",),"u"),(("L",),"u"),(("L","R"),"u"),(("R","L"),"u"),
                (("C",),"u"),(("L","C"),"u"),(("C","R"),"u"),(("C","L"),"d"),(("C","R"),"d"), 
                (("L","C","R"),"u"),(("L","C"),"d"),(("R","C"),"d"),(("L","C","R"),"d"),(("R","C","L"),"d")]
    for i in states:
        for j in states:
            for k in states:
                Rules[i,j,k] = ()
                #put in strands
                if ("L" in k[0]):
                    Rules[i,j,k] = Rules[i,j,k] + ("L",)
                if ("C" in j[0]):
                    Rules[i,j,k] = Rules[i,j,k] + ("C",)
                if ("R" in i[0]):
                    Rules[i,j,k] = Rules[i,j,k] + ("R",)
                #deal with crossing
                itrin = statetocrosstrin(i[0])
                        #set itrin to 0, 1, 2 depending on left
                jtrin = statetocrosstrin(j[0])
                        #set jtrin to 0, 1, 2 depending on center
                ktrin = statetocrosstrin(k[0])
                        #set ktrin to 0, 1, 2 depending on right
                if (i[1] == "u"):
                    itrin = 1 #non-crosssing
                if (j[1] == "u"):
                    jtrin = 1 #non-crosssing
                if (k[1] == "u"):
                    ktrin = 1 #non-crossing
                ijktrin = (9 * itrin + 3 * jtrin + ktrin) #0 to 26
                if ijktrin < 0 or 27 <= ijktrin:
                    raise Exception("Error parsing crossing status")
                if bincrossrule[ijktrin] == "0": 
                    #nothing needs to be done
                elif bincrossrule[ijktrin] == "1":
                    Rules[i,j,k] = tuple(reversed(Rules[i,j,k])) 
                        #this will need to be changed if more types of crossings allowed
                        #possibly will need to set ijktrin before putting in strands
                else:
                    raise Exception("Bad crossing rule")
                #start dealing with turning
                if Rules[i, j, k] == ():
                    Rules[i, j, k] = (Rules[i, j, k], "e")
                else: 
                    itrin = ["u","e","d"].index(i[1])
                    jtrin = ["u","e","d"].index(j[1])
                    ktrin = ["u","e","d"].index(k[1])
                    if (i[0] == ()):
                        itrin = 1 #empty
                    if (j[0] == ()):
                        jtrin = 1 #empty
                    if (k[0] == ()):
                        ktrin = 1 #empty
                    ijktrin = (9 * itrin + 3 * jtrin + ktrin) #0 to 26
                    if ijktrin < 0 or 27 <= ijktrin:
                        raise Exception("Error parsing turning status")
                    if binturnrule[ijktrin] == "0":
                        Rules[i,j,k] = reflectstate(Rules[i,j,k],"u")
                    elif binturnrule[iktrin] == "1":
                        Rules[i, j, k] = (Rules[i, j, k],"d")
                    else:
                        raise Exception("Bad turning rule")
    return(Rules)


def setupcelltodigittable ():
    celltodigit = dict()
    celltodigit[((),"e")] = 5 #empty
    celltodigit[(("L",),"u")] = 1 #1 left upright
    celltodigit[(("R",),"u")] = 2 #2 right upright
    celltodigit[(("L","R"),"u")] = 3 #3 left, right upright
    celltodigit[(("R","L"),"u")] = 4 #4 right, left upright (currently same as 3, but not for Friendship SCAs)
    celltodigit[(("L",),"d")] = 6 #6 left slanted (S)
    celltodigit[(("R",),"d")] = 7 #7 right slanted (Z)
    celltodigit[(("L","R"),"d")] = 8 #8 left, right slanted (S over Z)
    celltodigit[(("R","L"),"d")] = 9 #9 right, left slanted (Z over S)
    celltodigit[(("C",),"u")] = 10  #10 center upright
    celltodigit[(("L","C"),"u")] = 11 #11 left, center upright
    celltodigit[(("C","L"),"u")] = 11 #11 left, center upright JUST IN CASE!
    celltodigit[(("C","R"),"u")] = 12 #12 right, center upright
    celltodigit[(("R","C"),"u")] = 12 #12 right, center upright JUST IN CASE!
    celltodigit[(("C","L"),"d")] = 13 #13 center over left slanted (I over S) 
    celltodigit[(("C","R"),"d")] = 14 #14 center over right slanted (I over Z)
    celltodigit[(("L","C","R"),"u")] = 15 #15 left, center, right, upright
    celltodigit[(("R","C","L"),"u")] = 15 #15 left, center, right, upright JUST IN CASE! 
    celltodigit[(("L","C"),"d")] = 16 #16 left over center slanted (S over I)
    celltodigit[(("R","C"),"d")] = 17 #17 right over center slanted (Z over I)
    celltodigit[(("L","C","R"),"d")] = 18 #18 left, center, right slanted (S over I over Z)
    celltodigit[(("R","C","L"),"d")] = 19 #19 right, center, left slanted (Z over I over S)
    return(celltodigit)

def setupdigittocelltable ():
    digittocell = dict()
    digittocell[0] = ((),"e")  #0 dead (off the board)
    digittocell[1] = (("L",),"u") #1 left upright
    digittocell[2] = (("R",),"u") #2 right upright
    digittocell[3] = (("L","R"),"u") #3 left, right upright
    digittocell[4] = (("R","L"),"u") #4 right, left upright (currently same as 3, but not for Friendship SCAs)
    digittocell[5] = ((),"e") #empty
    digittocell[6] = (("L",),"d") #6 left slanted (S)
    digittocell[7] = (("R",),"d") #7 right slanted (Z)
    digittocell[8] = (("L","R"),"d") #8 left, right slanted (S over Z)
    digittocell[9] = (("R","L"),"d") #9 right, left slanted (Z over S)
    digittocell[10] = (("C",),"u") #10 center upright
    digittocell[11] = (("L","C"),"u") #11 left, center upright
    digittocell[12] = (("C","R"),"u") #12 right, center upright
    digittocell[13] = (("C","L"),"d") #13 center over left slanted (I over S) 
    digittocell[14] = (("C","R"),"d") #14 center over right slanted (I over Z)
    digittocell[15] = (("L","C","R"),"u") #15 left, center, right, upright
    digittocell[16] = (("L","C"),"d") #16 left over center slanted (S over I)
    digittocell[17] = (("R","C"),"d") #17 right over center slanted (Z over I)
    digittocell[18] = (("L","C","R"),"d") #18 left, center, right slanted (S over I over Z)
    digittocell[19] = (("R","C","L"),"d") #19 right, center, left slanted (Z over I over S)
    return(digittocell)



def writegollyrule (turningrule, crossingrule, brickstring):
    Rules = setupruletable(crossingrule, turningrule)
    Dtc = setupdigittocelltable()
    Ctd = setupcelltodigittable()
    filenamestring = g.getdir('rules') + "TCA" + brickstring + "-T%dC%d.rule" % (turningrule, crossingrule)
    outfile = open(filenamestring, 'w')
    print("@RULE TCA" + brickstring + "-T%dC%d\n" % (turningrule, crossingrule), file=outfile)
    print("@TABLE\n", file=outfile)
    print("n_states:20", file=outfile)
    print("neighborhood:hexagonal", file=outfile)
    print("symmetries:none", file=outfile)
#still need to fix this next bit!
'''
  #  print("var z={0,5} #dead or dummy cells", file=outfile)
  #  print("var y={0,5} #dead or dummy cells", file=outfile)
    print("var c={1,2,3,4,6,7,8,9,10} #live and not dummy", file=outfile)
    print("var d={1,2,3,4,6,7,8,9,10} #live and not dummy", file=outfile)
    print("var e={1,2,3,4,6,7,8,9,10} #live and not dummy", file=outfile)
    print("var h={0,1,2,3,4,5,6,7,8,9,10} #anything\n", file=outfile)
   # print("0,0,0,0,z,c,y,0,0,5 #dummy cells by parity", file=outfile)
    print("0,0,0,0,5,h,5,0,0,5 #dummy cells by parity", file=outfile)
    print("0,0,0,0,5,h,0,0,0,5 #dummy cells by parity", file=outfile)
    print("0,0,0,0,0,h,5,0,0,5 #dummy cells by parity", file=outfile)
    print("0,0,0,0,0,c,0,0,0,5 #dummy cells by parity", file=outfile) 
    print("0,0,0,c,0,0,0,h,0,5 # 'repair' dummies in the first row", file=outfile)
    print("0,0,0,h,0,0,0,c,0,5 # 'repair' dummies in the first row", file=outfile)
    print("0,0,0,0,c,d,e,0,0,0 #malformed", file=outfile)
    print("0,0,0,0,0,d,e,0,0,0 #malformed", file=outfile)
    print("0,0,0,0,c,d,0,0,0,0 #malformed\n", file=outfile) 
'''
    for i in range(0, 20):
        for j in range(0, 20):
            for k in range(0, 20):
                if (i !=0) or (j !=0) or (k !=0):
                    print("0,0,0,0,%d,z,%d,0,0,%d" % (k, i, Ctd[Rules[Dtc[i], Dtc[0], Dtc[k]]]), file=outfile)
    print("#anything else stays as is\n", file=outfile)
    return(outfile.close())

turningrule = int(g.getstring("Enter the Turning Rule number, from 0 to 134217727:",
                  "0", "SCA Turning Rule"))
                  
crossingrule = int(g.getstring("Enter the Crossing Rule number, from 0 to 134217727:",
                  "0", "SCA Crossing Rule"))

showbricks = (g.getstring("Would you like to show the brick boundaries (y/N)?",
                          "N", "Brick Boundaries")).upper()[0]
                  
if (showbricks == "Y"):
    brickstring = "bricks"
else:
    brickstring = ""
writegollyrule(turningrule, crossingrule, brickstring)
  
g.setrule("TCA" + brickstring + "-T%dC%d" % (turningrule, crossingrule))
g.show('Created '+"TCA" + brickstring + "-T%dC%d.rule" % (turningrule, crossingrule)+' and selected that rule.')
