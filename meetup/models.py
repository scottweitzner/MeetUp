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

    def get_skills(self):
        query = '''
        MATCH (u:User)-[:KNOWS]->(s:Skill) WHERE  u.email = {email}
        RETURN s.type AS type
        '''
        skills = graph.run(query, email=self.email).data()
        skill_list = []
        for skill in skills:
            skill_list.append(skill['type'])
        return skill_list

    def get_interests(self):
        query = '''
        MATCH (u:User)-[:INTERESTED_IN]->(s:Skill) WHERE  u.email = {email}
        RETURN s.type AS type
        '''
        interests = graph.run(query, email=self.email).data()
        interest_list = []
        for interest in interests:
            interest_list.append(interest['type'])
        return interest_list

    def create_event(self, title, event_type, event_date, event_time, max_participants, description):
        user = self.find()
        event = Node('Event', title=title, type=event_type, date=event_date, time=event_time, max_participants=max_participants, description=description)
        rel = Relationship(user, 'HOSTING', event)
        graph.merge(rel)


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%Y-%m-%d')



