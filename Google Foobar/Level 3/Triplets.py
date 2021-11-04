def solution3(l):

    total =0
    for j,y in enumerate(l):
        li_pairs =len( [ 1 for i,x in enumerate(l[:j] ) if y % x == 0 and j > i ])
        lk_pairs =len( [ 1 for k,z in enumerate( l[j:] ) if z % y == 0 and k+j > j ])
        #If we have li pairs then each connect to an lk pair so we have li_pairs*lk_pairs pairs
        #We aren't recounting any triplets as the middle is always "unique"
        total = total + li_pairs*lk_pairs

    return total
