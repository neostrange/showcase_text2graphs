from py2neo import Graph, Node, GraphService

#g= Graph("bolt://DESKTOP-F191J35.local:7687")
g= Graph("http://172.28.224.1:7474", auth=('neo4j', 'neo123'))
#g = Graph(host="DESKTOP-F191J35.local")
c= g.run("MATCH (n:NamedEntity) RETURN n LIMIT 25")
#graph = Graph(host='172.28.224.1:7687', auth=('neo4j', 'neo123'))




