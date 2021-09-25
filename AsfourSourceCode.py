"""
Name: Mohammad Asfour
AI: Project 2
"""

# createDic is a function that transform the data we have from list of lists to a dictionary
# the key of the dictionary represents a tile which is assigned a number which indicates the column,
# a symbol which indicates the cell, a set of letters which indicate the hyper cell (w,x,y,z),a different
# set of letters which indicate the row (A,B,C,D,E,F,G,H,I). The values are either an int that represents
# the assigned value or a list that contains the domain for that tile.
def createDic(lst):
    Dict = {}
    Length = len(lst)
    Letter = 'ABCDEFGHI'
    for i in range(Length):
        for j in range(Length):
            if (i < 3):              # check cell
                if (j < 3):
                    S = '+'
                elif (j < 6):
                    S = '*'
                else:
                    S = '&'
            elif (i < 6):
                if (j < 3):
                    S = '^'
                elif (j < 6):
                    S = '%'
                else:
                    S = '$'
            else:
                if (j < 3):
                    S = '#'
                elif (j < 6):
                    S = '@'
                else:
                    S = '!'
            if (i < 4 and i > 0):   # check hyper cell
                if (j < 4 and j > 0):
                    V = 'W'
                elif (j < 8 and j > 4):
                    V = 'Y'
                else:
                    V = 'N'
            elif (i < 8 and i > 4):
                if (j < 4 and j > 0):
                    V = 'X'
                elif (j < 8 and j > 4):
                    V = 'Z'
                else:
                    V = 'N'
            else:
                V = 'N'
            Val = S + Letter[i] + str(j) + V
            if (lst[i][j] == '0'):
                Dict[Val] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                Dict[Val] = int(lst[i][j])
    return Dict

# checks all the keys of the dictionary, if the tile contains a list it checks
# all the tiles in the same column, row, cell, and hyper cell. If they have an assigned value,
# then it removes that value from the domain of the current tile
def forwCheck(forDict):
    Dict = forDict.copy()
    for i in Dict.keys():
        if (type(Dict[i]) == list):
            for j in Dict.keys():
                if (i[0] == j[0]) or (i[1] == j[1]) or (i[2] == j[2]):
                    if (type(Dict[j]) == int):
                        try:
                            Dict[i].remove(Dict[j])
                            if len(Dict[i]) == 1:
                                Dict[i] = Dict[i][0]
                                Dict = forwCheck(Dict)
                        except:                     # in case Dict[j] is not in the list
                            None
                elif (i[3] != 'N' and j[3] != 'N'): # if it's inside one of the hyper cells
                    if (i[3] == j[3]):
                        if (type(Dict[j]) == int):
                            try:
                                Dict[i].remove(Dict[j])
                                if len(Dict[i]) == 1:
                                    Dict[i] = Dict[i][0]
                                    Dict = forwCheck(Dict)
                            except:                  # in case Dict[j] is not in the list
                                None
        elif (type(Dict[i]) == int):
            for j in Dict.keys():
                if (i[0] == j[0]) or (i[1] == j[1]) or (i[2] == j[2]):
                    if (type(Dict[j]) == int) & (j != i):
                        if Dict[i] == Dict[j]:
                            return False
                elif (i[3] != 'N' and j[3] != 'N'): # if it's inside one of the hyper cells
                    if (i[3] == j[3]):
                        if (type(Dict[j]) == int) & (j != i):
                            if Dict[i] == Dict[j]:
                                return False
    return Dict


# returns the total domain
def Domain(Dict):
    Tot = 0
    for i in Dict.keys():
        try:
            Tot += len(Dict[i])
        except:
            None
    return Tot


# checks if a certain value can be assigned to a tile by checking all the tiles in the
# same row, column, cell and hyper cell.
def ValidTile(Dict, key, num):
    for i in Dict.keys():
        if (i[0] == key[0]) or (i[1] == key[1]) or (i[2] == key[2]):
            if num == Dict[i]:
                return False
        elif (i[3] != 'N' and key[3] != 'N'):
            if (i[3] == key[3]):
                if num == Dict[i]:
                    return False
    return True


# returns a list of the tiles in the dictionary with the shortest domains
def shortestDom(Dict):
    L = 10
    res = False
    for i in Dict.keys():
        if (type(Dict[i]) == list):
            if (len(Dict[i]) < L):
                res = [i]
                L = len(Dict[i])
            elif len(Dict[i]) == L:
                res.append(i)
    return res


# returns the degree of a certain tile -- the number of tiles in the same row, column,
# cell and hyper cell which have not been assigned a value yet
def Select_unaasigned_variable(Dict, key):
    tot = 0
    for i in Dict.keys():
        if (i[0] == key[0]) or (i[1] == key[1]) or (i[2] == key[2]):
            if type(Dict[i] == list):
                tot += 1
        elif (i[3] != 'N' and key[3] != 'N'):
            if (i[3] == key[3]):
                if type(Dict[i] == list):
                    tot += 1
    return tot


# Backtracking algorithm to solve the puzzle
def BackTrackSolve(Dict):
    curr = shortestDom(Dict)                          # Finds the smallest domain tile
    if curr == False:                                 # All tiles have an assigned value which means the puzzle has been solved
        return Dict
    elif len(curr) == 1:                              # There is only one tile with the shortest domain
        key = curr[0]
    else:                                             # There are multiple tiles with the shortest domain
        key = curr[0]
        Length = Select_unaasigned_variable(Dict, key)
        for i in range(1, len(curr)):                 # Use mrv and degree heuristic to determine which tile to do first
            if Select_unaasigned_variable(Dict, curr[i]) > Length:
                key = curr[i]                         # If there are more than one variables left after applying
                                                      # the two heuristics, arbitrarily choose one (the first one)
    lst = Dict[key]
    for j in range(len(lst)):
        if ValidTile(Dict, key, lst[j]):
            Dict[key] = lst[j]                        # if value is good try assign it to the tile
            nDict = BackTrackSolve(Dict)              # Once a value is assigned re-run algorithm on new dictionary
            if nDict != False:                        # if all successive values are added succesfuly return the dictionary
                return nDict
    Dict[key] = lst                                   # if the backtracking failed then replace the tile with its domain
    return False                                      # return false if none of the values in the domain are good

# Displays the numbers in a good visual way
def Display(Dict):
    count = 0
    c = 0
    for i in Dict.keys():
        if type(Dict[i]) == int:
            print(Dict[i], end=" ")
        else:
            print(' ', end=" ")
        count += 1
        if (count == 3) or (count == 6):
            print("|", end=" ")
        elif count == 9:
            print()
            count = 0
            c += 1
            if c == 3 or c == 6:
                print("---------------------")


Fil = input("Which file do you want to analyze? ")  # Type the number of the file you want to analyze
file = open('input' + str(Fil) + '.txt', 'r')       # read the txt file
output = open('output' + str(Fil) + '.txt', 'w')    # create an output text file

# convert text file into lists
data = []
for line in file:
    data.append(line.split())             # transform it into a list of lists

DicData = createDic(data)                 # Convert the list into a dictionary

DicDataF = forwCheck(DicData)             # Perform Forward Checking

DicDataB = BackTrackSolve(DicDataF)       # Perform backchecking

Display(DicDataF)
print('------------')
Display(DicDataB)
print('------------')

# Write the output board in a text file
count = 0
for i in DicDataB.keys():
   output.write(str(DicDataB[i]) + " ")
   count += 1
   if count == 9:
       output.write("\n")
       count = 0

output.close()
file.close()