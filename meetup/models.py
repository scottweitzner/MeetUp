from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import uuid
import constants

# where bulk of action takes place

url = 'http://hobby-amiglogeoeaggbkemomdkmpl.dbs.graphenedb.com:24789'
neo4j_username = "main"
neo4j_password = constants.NEO4J_PASS

graph = Graph(url + '/db/data/', username=neo4j_username, password=neo4j_password)


class User:
    def __init__(self, username):
        self.username = username

    def find(self):
        user = graph.find_one('User', 'username', self.username)
        return user

    def register(self, password):
        if not self.find():
            user = Node('User', username=self.username, password=bcrypt.encrypt(password))
            graph.create(user)
            return True
        else:
            return False

    def verify_password(self, password):
        user = self.find()
        if user:
            return bcrypt.verify(password, user['password'])

    def add_post(self, title, tags,  text):
        user = self.find()
        post = Node(
            'Post',
            id=str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp=timestamp(),
            date=date()
        )
        rel = Relationship(user, 'PUBLISHED', post)
        graph.create(rel)

        tags = [tag.strip() for tag in tags.lower().split(",")]
        for name in set(tags):
            tag = Node('Tag', name=name)
            graph.merge(tag)

            rel = Relationship(post, 'TAGGED_BY', tag)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()
        post = graph.find_one('Post', 'id', post_id)
        graph.merge(Relationship(user, 'LIKED', post))

    def get_recent_posts(self):
        query = '''
        MATCH (user:USER)-[:PUBLISHED]->(post:POST)-[:TAGGED_BY]->(tag:Tag)
        WHERE user.username = {username}
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT 5
        '''

        return graph.run(query, username=self.username)

    def get_similar_users(self):
        query = '''
        MATCH (you:User)-[:PUBLISHED]->(post:Post)-[:TAGGED_BY]->(tag:Tag),
            (they:USER)-[:PUBLISHED]->(post:Post)-[:TAGGED_BY]->(tag)
        WHERE you.username = {username} AND you <> they
        WITH they, COLLECT(DISTINCT tag.name) AS tags
        ORDER BY SIZE(tags) DESC LIMIT 3
        RETURN they.username AS similar_user, tags
        '''
        return graph.run(query, username=self.username)

    def get_commonality_of_user(self, other):
        query = '''
        MATCH (they:USER { username: {they} })
        MATCH (you:USER { username: {you} })
        OPTIONAL MATCH (they)-[:PUBLISHED]->(:Post)-[:TAGGED_BY]->(tag:Tag),
                        (you)-[:PUBLISHED]->(:Post)-[:TAGGED_BY]->(tag)
        RETURN SIZE( (they)-[:LIKED]->(:Post)<-[:PUBLISHED]-(you) ) AS LIKES,
            COLLECT( DISTINCT tag.name ) AS tags
        '''
        return graph.run(query, you=self.username, they=other)


def get_todays_recent_posts():
    query = '''
    MATCH (user:User)-[:PUBLISHED]->(post:Post)-[:TAGGED_BY]->(tag:Tag)
    WHERE post.date = {today}
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT 5
    '''
    return graph.run(query, today=date())


def timestamp():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    delta = now - epoch
    return delta.total_seconds()


def date():
    return datetime.now().strftime('%Y-%m-%d')


################################################################################
#  My Methods To Showcase Neo4j Capabilities
################################################################################
def get_sentiment_over_time(company_ticker):
    query = '''
    MATCH ()-[W:WROTE]->(a:Article)-[M:MENTIONS]->(c:Company) WHERE c.ticker = {ticker}
    RETURN W.daysAgo AS daysAgo, M.sentiment AS sentiment, c.name AS company
    ORDER BY daysAgo
    '''
    data = graph.run(query, ticker=company_ticker).data()
    return data
