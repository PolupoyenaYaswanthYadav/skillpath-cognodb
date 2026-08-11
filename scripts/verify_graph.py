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

NODE_LABELS = [
    "Role",
    "Skill",
    "Technology",
    "Project",
    "Company",
    "Course",
]


def main():
    with driver.session() as session:
        print("\n=== NODE COUNTS ===\n")

        for label in NODE_LABELS:
            result = session.run(
                f"MATCH (n:{label}) RETURN count(n) AS count"
            )
            count = result.single()["count"]
            print(f"{label:15} {count}")

        print("\n=== RELATIONSHIP COUNTS ===\n")

        result = session.run(
            """
            MATCH ()-[r]->()
            RETURN type(r) AS relationship, count(r) AS count
            ORDER BY relationship
            """
        )

        for record in result:
            print(
                f"{record['relationship']:25} {record['count']}"
            )

        print("\n=== TOTALS ===\n")

        result = session.run(
            """
            MATCH (n)
            WITH count(n) AS nodes
            MATCH ()-[r]->()
            RETURN nodes, count(r) AS relationships
            """
        )

        record = result.single()

        print(f"Nodes:         {record['nodes']}")
        print(f"Relationships: {record['relationships']}")

    driver.close()


if __name__ == "__main__":
    main()
