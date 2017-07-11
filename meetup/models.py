from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import constants

# where bulk of action takes place
protocol = 'http://'
url = 'hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789'
neo4j_username = "main"
neo4j_password = constants.NEO4J_PASS

authenticate(url, neo4j_username, neo4j_password)
graph = Graph(protocol + url, bolt=False)


class User:
    def __init__(self, email):
        self.email = email

    def find(self):
        user = graph.find_one('User', 'email', self.email)
        return user

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%Y-%m-%d')



