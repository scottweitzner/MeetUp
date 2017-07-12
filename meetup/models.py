from py2neo import Graph, Node, Relationship, authenticate
from passlib.hash import bcrypt
from datetime import datetime
import constants
import NLU_module as Watson

from difflib import get_close_matches

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
            skill_list.append(skill['type'].encode('ascii', 'ignore'))
        return skill_list

    def get_interests(self):
        query = '''
        MATCH (u:User)-[:INTERESTED_IN]->(s:Skill) WHERE  u.email = {email}
        RETURN s.type AS type
        '''
        interests = graph.run(query, email=self.email).data()
        interest_list = []
        for interest in interests:
            interest_list.append(interest['type'].encode('ascii', 'ignore'))
        return interest_list

    def create_event(self, title, event_type, event_date, event_time, max_participants, description):
        user = self.find()
        event = Node('Event', title=title, type=event_type, date=event_date, time=event_time, max_participants=max_participants, description=description)
        rel = Relationship(user, 'HOSTING', event)
        graph.merge(rel)

    def add_skills(self, skills):
        user = self.find()
        for skill in skills:
            new_skill = Node('Skill', type=skill)
            rel = Relationship(user, 'KNOWS', new_skill)
            graph.merge(rel)

    def add_interests(self, interests):
        user = self.find()
        for interest in interests:
            new_interest = Node('Skill', type=interest)
            rel = Relationship(user, 'INTERESTED_IN', new_interest)
            graph.merge(rel)


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%Y-%m-%d')


def get_skill_and_interest_suggestions(bio):
    raw_suggestions = Watson.get_watson_keywords(bio)
    skills = []
    for raw in raw_suggestions:
        skills.append(raw['text'].encode('ascii', 'ignore'))
    return skills


def filter_duplicate_skills(raw, skills):

    lower_skills = map(lambda x: x.lower(), skills)

    filtered = []
    for keyword in raw:
        if str.lower(keyword) not in get_close_matches(str.lower(keyword), lower_skills, cutoff=0.5):
            filtered.append(keyword)

    return filtered


def filter_duplicate_interests(raw, interests):

    lower_interests = map(lambda x: x.lower(), interests)

    filtered = []
    for keyword in raw:
        if str.lower(keyword) not in get_close_matches(str.lower(keyword), lower_interests, cutoff=0.5):
            filtered.append(keyword)

    return filtered
