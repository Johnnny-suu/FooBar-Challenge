def solution(src, dest):
    from itertools import permutations
    class node:
        def __init__(self,loc,move):
            self.loc = loc
            self.move = move

    moves = [x for x in [p for p in permutations([1,2,-1,-2],r=2)] if abs(x[0]) != abs(x[1])]
    isExplored = { i:False for i in range(0,64)}
    xy_co = { 8*i+j:(i,j) for i in range(8) for j in range(8)}
    q = [node(src,0)]
    isExplored[src]= True
    while q != []:
        n = q.pop(0)
        if n.loc == dest:
            return int(n.move)
        else:# Get list of legal moves in xy domain
            for xy in [tuple(map(sum, zip(xy_co[n.loc],move))) for move in moves if min(tuple(map(sum, zip(xy_co[n.loc],move)))) >= 0 and max(tuple(map(sum, zip(xy_co[n.loc],move)))) < 8]:
                loc = xy[0]+8*xy[1]
                if isExplored[loc] == False:
                    isExplored[loc]=True
                    q.append(node(loc,n.move+1))


'''
Better:
-Did not need class for node. The loc would have sufficed
-For the isExplored dict, we could have had -1 as unexplored and any integer greater -1 stored as the shortest # of moves to get to that loc from src
that way -->
isExplored[loc] = isExplored[n]+1
q.append(loc)

so the exit criteria could be
if n = dest #as n is now the location value,
    return isExplored[loc] # Returns the shortest # of moves to get from src to dest
Should have added an exit criteria in the else once a move to get to dest is legal
'''
