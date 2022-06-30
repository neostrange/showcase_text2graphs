from py2neo import Graph
from py2neo import *

graph = Graph("bolt://192.168.1.13:7687", auth=("neo4j", "neo123"))
#graph.run("UNWIND range(1, 3) AS n RETURN n, n * n as n_sq")
#c= graph.run("MATCH (n) RETURN n")

#for a in c:
#    print (a)
    

a = Node("Frame", text="verb", span="", startIndex="", endIndex="")
b = Node("FrameArgument", type="", text="Bob", span="", startIndex="", endIndex="")
c = Node("Person", name="Carol")
KNOWS = Relationship.type("KNOWS")
ab = KNOWS(a, b)
ba = KNOWS(b, a)
ac = KNOWS(a, c)
ca = KNOWS(c, a)
bc = KNOWS(b, c)
cb = KNOWS(c, b)
friends = ab | ba | ac | ca | bc | cb
#g = Graph()
graph.create(friends)