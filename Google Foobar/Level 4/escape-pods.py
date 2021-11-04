
def solution(entrances, exits, path):
    import numpy as np

    class network:
        def __init__(self,path=[],entrances = [0], exits = [1]):
            self.nodes = []
            self.edges = {} #Edges is a dict where the (out,in) is the key and current capcity is the value
            self.path = np.array(path)
            self.flow = 0
            if self.path.shape!= 0: #Check if empty
                self.addNodes()
                self.addEdges()
                self.createSource(entrances)
                self.createTerminal(exits)

        def createSource(self,entrances):
            if len(entrances)>1:
                self.src = -1
                self.nodes.insert(0,-1)

                capacity = np.sum(self.path[entrances,:],axis = 1) #Get the total output of the entrance nodes --> row sum

                self.edges.update({ (-1,entrances[i]):c for i,c in enumerate(capacity) })
            else:
                self.src = entrances[0]
        def createTerminal(self,exits):
            if len(exits)>1:
                self.sink = self.path.shape[0]
                self.nodes.insert(self.sink,self.sink)
                capacity = np.sum(self.path[:,exits],axis = 0) # Get total going into exits --> col sum
                self.edges.update({ (exits[i],self.sink):c  for i,c in enumerate(capacity) })
            else:
                self.sink = exits[0]

        def addNodes(self):
            self.nodes.extend(list(range(len(self.path))))
        def addEdges(self):
            #List of nested tuples of (from,to),capacity
            i,j = np.nonzero(self.path)
            self.edges.update({ (i[k],j[k]) : self.path[i[k]][j[k]] for k in range(len(i)) })
        def bfs(self):
            #Find shortest path from src to sink.
            visit_dict = {i:None for i in self.nodes }
            visit_dict[self.src] = self.src # use -1 as meaning source
            shortest_path = []
            q = [self.src]
            while q != []:
                n = q.pop(0)
                if n == self.sink:
                    x = n
                    while(x != self.src):
                        shortest_path.append( (visit_dict[x],x) )
                        x = visit_dict[x]
                    shortest_path.reverse()
                    return shortest_path
                else:
                    pass
                    for start,end in iter([key for key in self.edges.keys() if n in key and self.edges[key] > 0]):
                        if visit_dict[end] == None:
                            visit_dict[end] = start
                            q.append(end)
            return None
        def applyMinFlow(self,shortest_path):

            df = min([self.edges[edge] for edge in shortest_path])
            for edge in shortest_path:
                #Update Capacities
                self.edges[edge] -= df
            self.flow += df

    def EdmondsKarp(G):
        shortest_path = G.bfs()
        while shortest_path != None:
            G.applyMinFlow(shortest_path)
            shortest_path = G.bfs()
        return G.flow


    #Create a single Source/Destination Node to path if multiple entrances/exits exist


    G= network(path,entrances,exits)
    return EdmondsKarp(G)


    # print([key for key in G.edges.keys() if 0 == key[0] ])
    # for abcd,dz in iter([key for key in G.edges.keys() if 0 == key[0] ]):
    #     print('hi')

def main():
    entrances = [0, 1]
    exits = [4, 5]
    path = [
    [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
    [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
    [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
    [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
    [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
    [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
    ]
    print(solution(entrances, exits, path))
    print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]))
main()
