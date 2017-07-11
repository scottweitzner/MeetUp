from py2neo import Graph, Node, Relationship, authenticate
import constants

protocol = 'http://'
url = 'hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789'
neo4j_username = "main"
neo4j_password = constants.NEO4J_PASS

authenticate(url, neo4j_username, neo4j_password)
graph = Graph(protocol + url, bolt=False)


query = '''
    CREATE (:TEST {testid:2})
    '''

graph.run(query)
