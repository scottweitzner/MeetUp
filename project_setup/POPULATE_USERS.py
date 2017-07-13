from py2neo import Graph, Node, Relationship, authenticate
import constants
import json
from passlib.hash import bcrypt

protocol = 'http://'
url = 'hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789'
neo4j_username = "main"
neo4j_password = constants.NEO4J_PASS
authenticate(url, neo4j_username, neo4j_password)
graph = Graph(protocol + url, bolt=False)

with open('USERS.json') as data_file:
    data = json.load(data_file)

    for user in data:
        email = user['email']
        password = bcrypt.encrypt(user['password'])
        school = user['school']
        position = user['position']
        group = user['group']
        name = user['name']
        bio = user['bio']

        User = Node("User", name=name, email=email, password=password, school=school, position=position, group=group, bio=bio)

        for interest in user['interests']:
            Interest = Node("Skill", type=interest)
            rel = Relationship(User, 'INTERESTED_IN', Interest)
            # graph.merge(rel)

        for skill in user['skills']:
            Skill = Node("Skill", type=skill)
            rel = Relationship(User, "KNOWS", Skill)
            # graph.merge(rel)
