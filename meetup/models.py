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

    def attend_event(self, title, event_date, event_time):
        user = self.find()
        query = '''
        MATCH (e:Event) WHERE e.title={title} AND e.date={date} AND e.time={time}
        RETURN e
        '''
        event = graph.run(query, title=title, date=event_date, time=event_time)

        rel = Relationship(user, 'ATTENDING', event)
        graph.merge(rel)

    def remove_from_event(self, title, event_date, event_time):
        user = self.find()
        query = '''
        MATCH (u:User)-[r:ATTENDING]->(e:Event) WHERE e.title={title} AND e.date={date} AND e.time={time} AND u.email = {email}
        DETACH DELETE r
        '''
        graph.run(query, title=title, date=event_date, time=event_time, email=user['email'])

    def get_events_going_to(self):
        user = self.find()
        query = '''
        MATCH (u:User)-[:ATTENDING]->(e:Event)<-[:HOSTING]-(host:User) WHERE u.email={user_email}
        RETURN host.name AS host_name, host.email AS host_email, e AS Event
        '''
        raw = graph.run(query, user_email=user['email']).data()
        return raw_to_event_list(raw)

    def get_events_not_going_to(self):
        user = self.find()
        query = '''
                MATCH (u:User)-[:ATTENDING]->(e:Event) WHERE u.email={email}
                WITH collect(DISTINCT e) as events_attended
                MATCH (host:User)-[:HOSTING]->(event:Event)
                WHERE NOT event IN events_attended AND host.email <> {email}
                RETURN host.name AS host_name, host.email AS host_email, event AS Event
                '''

        raw = graph.run(query, email=user['email']).data()

        print raw
        return raw_to_event_list(raw)

    def get_recommended_events(self):
        user = self.find()
        query = '''
                MATCH (u:User)-[:INTERESTED_IN]->(s:Skill)<-[:KNOWS]-(host:User) WHERE u.email={email}
                MATCH (host)-[:HOSTING]->(e:Event) WHERE NOT (u)-->(e)
                RETURN host.name AS host_name, host.email AS host_email, e as Event , COLLECT(s.type) AS skills
                '''

        raw = graph.run(query, email=user['email']).data()

        events = []
        for obj in raw:
            event_obj = obj['Event']

            reasons = []
            print obj
            for reason in obj['skills']:
                reasons.append('you have an interest in ' + reason + ' and ' + obj['host_name'] + ' has that as a skill' )

            events.append(
                {
                    'host': obj['host_name'],
                    'host_email': obj['host_email'],
                    'title': event_obj['title'],
                    'date': event_obj['date'],
                    'time': event_obj['time'],
                    'type': event_obj['type'],
                    'max_participants': event_obj['max_participants'],
                    'description': event_obj['description'],
                    'reasons': reasons
                }
            )
        return events


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


def get_all_events():
    query = '''
    MATCH (u:User)-[:HOSTING]->(e:Event)
    RETURN u.name AS host_name, u.email AS host_email, e as Event
    '''
    raw = graph.run(query).data()
    return raw_to_event_list(raw)


def raw_to_event_list(raw):
    events = []
    for obj in raw:
        event_obj = obj['Event']
        events.append(
            {
                'host': obj['host_name'],
                'host_email': obj['host_email'],
                'title': event_obj['title'],
                'date': event_obj['date'],
                'time': event_obj['time'],
                'type': event_obj['type'],
                'max_participants': event_obj['max_participants'],
                'description': event_obj['description']
            }
        )
    return events


