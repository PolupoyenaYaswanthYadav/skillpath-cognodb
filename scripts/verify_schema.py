import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")


driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD),
)

try:
    with driver.session() as session:
        result = session.run("SHOW CONSTRAINTS")

        records = list(result)

        print(f"Found {len(records)} constraints:")

        for record in records:
            print(record)

finally:
    driver.close()
