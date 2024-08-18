# Implements Stranded Cellular Automata (first defined in https://archive.bridgesmathart.org/2016/bridges2016-127.html) in Golly.
#
# Rules/SCA45-shared.rule and/or Rules/SCA45bricks-shared.rule should be in your personal rule directory.
# Scripts/write-SCA45-rule.py takes a turning rule number and a crossing
# rule number, generates a Golly rule file in your personal rule
# directory, and then loads it up.
# 
# Diamond grid, proceeds from SE to NW, for compatibility with future hex version.
#
# contact:  holden@rose-hulman.edu



import golly as g

def setupruletable (crossingrule, turningrule):
    Rules = dict()
    bincrossrule = bin(crossingrule + 512)[-1:2:-1] #convert to binary in reverse
    binturnrule = bin(turningrule + 512)[-1:2:-1] #convert to binary in reverse
    states = [((),"e"),(("R",),"d"),(("L",),"d"),(("L","R"),"d"),(("R","L"),"d"),(("R",),"u"),(("L",),"u"),(("L","R"),"u"),(("R","L"),"u")]
    for i in states:
        for j in states:
            for k in states:
                if not(("R" in i[0]) or ("L" in k[0])):
                    Rules[i, j, k] = () #nothing pointing into the cell
                elif ("R" in i[0]) and ("L" not in k[0]):
                    Rules[i, j, k] = ("R",) #only right pointing into the cell
                elif ("R" not in i[0]) and ("L" in k[0]):
                    Rules[i, j, k] = ("L",) #only left pointing into the cell  
                else: #both pointing into the cell, deal with crossing first
                    itrin = [("L","R"),("R",),("R","L")].index(i[0])
                        #set itrin to 0, 1, 2 depending on left
                    ktrin = [("R","L"),("L",),("L","R")].index(k[0])
                        #set ktrin to 0, 1, 2 depending on right
                    if (i[1] == "u"):
                        itrin = 1 #non-crosssing
                    if (k[1] == "u"):
                        ktrin = 1 #non-crossing
                    iktrin = 3 * itrin + ktrin #0 to 8
                    if iktrin < 0 or 8 < iktrin:
                        raise
                    if bincrossrule[iktrin] == "0": 
                        Rules[i, j, k] = ("L","R")
                    elif bincrossrule[iktrin] == "1":
                        Rules[i, j, k] = ("R","L")
                    else:
                        raise Exception("Bad crossing rule")
                #start dealing with turning
                if Rules[i, j, k] == ():
                    Rules[i, j, k] = (Rules[i, j, k], "e")
                else: 
                    itrin = ["u","e","d"].index(i[1])
                    ktrin = ["u","e","d"].index(k[1])
                    if (i[0] == ()):
                        itrin = 1 #empty
                    if (k[0] == ()):
                        ktrin = 1 #empty
                    iktrin = 3 * itrin + ktrin #0 to 8
                    if iktrin < 0 or 8 < iktrin:
                        raise
                    if binturnrule[iktrin] == "0":
                        if Rules[i, j, k] == ("R",):
                            Rules[i, j, k] = (("L",),"u")
                        elif Rules[i, j, k] == ("L",):
                            Rules[i, j, k] = (("R",),"u")
                        else:
                            Rules[i, j, k] = (Rules[i, j, k],"u")
                    elif binturnrule[iktrin] == "1":
                        Rules[i, j, k] = (Rules[i, j, k],"d")
                    else:
                        raise Exception("Bad turning rule")
    return(Rules)


def setupcelltodigittable ():
    celltodigit = dict()
    celltodigit[((),"e")] = 5
    celltodigit[(("L",),"u")] = 1
    celltodigit[(("R",),"u")] = 2
    celltodigit[(("L","R"),"u")] = 3
    celltodigit[(("R","L"),"u")] = 4
    celltodigit[(("L",),"d")] = 6
    celltodigit[(("R",),"d")] = 7
    celltodigit[(("L","R"),"d")] = 8
    celltodigit[(("R","L"),"d")] = 9
    return(celltodigit)


def setupdigittocelltable ():
    digittocell = dict()
    digittocell[0] = ((),"e")
    digittocell[1] = (("L",),"u")
    digittocell[2] = (("R",),"u")
    digittocell[3] = (("L","R"),"u")
    digittocell[4] = (("R","L"),"u")
    digittocell[5] = ((),"e")
    digittocell[6] = (("L",),"d")
    digittocell[7] = (("R",),"d")
    digittocell[8] = (("L","R"),"d")
    digittocell[9] = (("R","L"),"d")
    digittocell[10] = ((),"e")
    return(digittocell)



def writegollyrule (turningrule, crossingrule, brickstring):
    Rules = setupruletable(crossingrule, turningrule)
    Dtc = setupdigittocelltable()
    Ctd = setupcelltodigittable()
    filenamestring = g.getdir('rules') + "SCA45" + brickstring + "-T%dC%d.rule" % (turningrule, crossingrule)
    outfile = open(filenamestring, 'w')
    print("@RULE SCA45" + brickstring + "-T%dC%d\n" % (turningrule, crossingrule), file=outfile)
    print("@TABLE\n", file=outfile)
    print("n_states:10", file=outfile)
    print("neighborhood:vonNeumann", file=outfile)
    print("symmetries:none", file=outfile)
  #  print("var z={0,5} #dead or dummy cells", file=outfile)
  #  print("var y={0,5} #dead or dummy cells", file=outfile)
    print("var c={1,2,3,4,6,7,8,9} #live and not dummy", file=outfile)
  #  print("var d={1,2,3,4,6,7,8,9} #live and not dummy", file=outfile)
  #  print("var e={1,2,3,4,6,7,8,9} #live and not dummy", file=outfile)
    print("var h={0,1,2,3,4,5,6,7,8,9} #anything\n", file=outfile)
    print("0,c,0,0,h,5 # 'repair' bricks in the first row", file=outfile)
    print("0,h,0,0,c,5 # 'repair' bricks in the first row", file=outfile)
    for i in range(0, 10):
        for k in range(0, 10):
            if (i !=0) or (k !=0):
                print("0,0,%d,%d,0,%d" % (k, i, Ctd[Rules[Dtc[i], Dtc[0], Dtc[k]]]), file=outfile)
    print("#anything else stays as is\n", file=outfile)
    return(outfile.close())

turningrule = int(g.getstring("Enter the Turning Rule number, from 0 to 511:",
                  "0", "SCA Turning Rule"))
                  
crossingrule = int(g.getstring("Enter the Crossing Rule number, from 0 to 511:",
                  "0", "SCA Crossing Rule"))

showbricks = (g.getstring("Would you like to show the brick boundaries (y/N)?",
                          "N", "Brick Boundaries")).upper()[0]
                  
if (showbricks == "Y"):
    brickstring = "bricks"
else:
    brickstring = ""
writegollyrule(turningrule, crossingrule, brickstring)

width = int(g.getstring("This time only, load the rule at what width (0 for infinite)?", "0", "Width"))
  
g.setrule("SCA45" + brickstring + "-T%dC%d:T%d,1000000+%d" % (turningrule, crossingrule, width, width))
g.show('Created '+"SCA45" + brickstring + "-T%dC%d.rule" % (turningrule, crossingrule)+' and selected that rule with bounded grid T%d,1000000+%d.' % (width,width))
