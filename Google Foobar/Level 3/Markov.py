def solutionWorks(n):
    import numpy as np
    from numpy import ma
    from fractions import Fraction
    n = np.array(n)
    d = np.shape(n)[0]
    connections = np.nonzero(n) # Get 2 arrays first are rows, second is cols
    row_sum = np.sum(n,axis=1)
    terminal_states = [i for i,j in enumerate(row_sum) if j == 0]
    #FIND OBSERVABLE MARKOV CHAIN FROM s0
    l = [0]
    for node in range(d):
        #append the next node if there is a connection to the current node and it is no in l yet
        l = l + [connections[1][i] for i,j in enumerate(connections[0]) if j == l[node] and connections[1][i] not in l]
        if l[node] == l[-1] and l[node] in terminal_states:
            break
    l.sort()
    #Delete states that are unreachable from s0

    #REMOVE UNOBSERVABLE STATES,REFORM MATRIX INTERMS OF Q,R. CAN PROBABLY JUST USE SLICING

    m = np.zeros(n.shape)
    notInM = [x for x in range(d) if x not in (l)]
    if 0 in terminal_states:
        return [1] + [0 for terminal in terminal_states[1:]] +[1]
    for unobser in notInM:
        m[unobser,unobser] = 1
    m = ma.compress_rowcols(ma.masked_array(n,m))
    #print(m)
    unobser_sum = row_sum[notInM]
    row_sum = np.delete(row_sum,notInM)

    mask = np.where(row_sum > 0,True,False)
    lcm = np.lcm.reduce(row_sum[mask])
    deno = np.array([lcm//row_sum[i] if row_sum[i] != 0 else 0 for i in range(len(row_sum))])

    #array masking and slicing for sure is better
    m = np.array([m[i,:]*deno[i] for i in range(len(deno)) ])
    ind = np.lexsort((l,~mask))
    l = (np.array(l)[ind])
    m = m[ind,:]
    m = m[:,ind]
    mask = mask[ind]
    swaps = [ (i,j) for i,j in zip(ind,~mask)]
    Q,R  =np.split( m[mask],[len(mask[mask])],axis = 1)

    #GAUSSIAN REDUCTION TO GET INVERSE need Q,R,ind, terminal states,l, not in M,lcm
    G = np.array(np.append((lcm*np.identity(Q.shape[0]) - Q), np.identity(Q.shape[0]),axis = 1),dtype='int')
    check = lcm*np.identity(Q.shape[0]) - Q
    factors_d = G[0][0]*np.ones(G.shape[0],dtype = 'int')
    #Forwards Propagate
    for i in range(1,G.shape[0]):
        G[i:][:] = (G[i-1][i-1]*G[i:][:]) - (G[i:,i-1,np.newaxis]*G[i-1,:])
        gcd_rows = np.array( [np.gcd.reduce( G[j, np.nonzero(G[j,:])[0] ] ) for j in range(i, G.shape[0] )] )
        G[i:][:] = G[i:,:]//gcd_rows[:,np.newaxis]
        factors_d[i:] = G[i][i]
    #Backwards Propagate
    for i in range(G.shape[0]-1,0,-1):
        G[:i][:] = (G[i][i]*G[:i][:]) - (G[:i,i,np.newaxis]*G[i,:])
        gcd_rows = np.array([np.gcd.reduce( G[j,np.nonzero(G[j,:])[0] ]) for j in range(0,i)  ])
        G[:i][:] = G[:i,:]//gcd_rows[:,np.newaxis]
        factors_d[:i] = G[i-1][i-1]
    inv = G[:,G.shape[0]:]
    H = np.matmul(inv,R)

#Probability and sorting output
    hitting_prob = [Fraction(f,int(factors_d[0])) for f in H[0][:]]
    p_lcm = np.lcm.reduce([f.denominator for f in hitting_prob])

    hitting_prob = [(p_lcm//f.denominator*f.numerator,state) for f,state in zip(hitting_prob,[t for t in l if t in terminal_states] )]
    unobser_term = [(0,i) for i in [nt for nt in notInM if nt in terminal_states]]

    return [p[0] for p in sorted(hitting_prob+unobser_term,key = lambda x:x[1])] + [p_lcm]