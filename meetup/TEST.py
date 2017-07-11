from py2neo import Graph, Node, Relationship, authenticate
import constants

url = 'http://hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789'
neo4j_username = "main"
neo4j_password = constants.NEO4J_PASS

authenticate("hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789", neo4j_username, neo4j_password)
graph = Graph("http://hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789", bolt=False)

# graph = Graph(url + '/db/data/', username=neo4j_username, password=neo4j_password)

query = '''
    CREATE (:TEST {testid:2})
    '''

graph.run(query)
