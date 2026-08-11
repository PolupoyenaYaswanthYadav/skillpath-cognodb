from neo4j import GraphDatabase

from backend.config import (
    COGNODB_PASSWORD,
    COGNODB_URI,
    COGNODB_USERNAME,
)


class Database:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USERNAME, COGNODB_PASSWORD),
        )

    def verify_connectivity(self):
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def execute(self, query: str, **parameters):
        with self.driver.session() as session:
            result = session.run(query, **parameters)
            return [record.data() for record in result]


db = Database()
