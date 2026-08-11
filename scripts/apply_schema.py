import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

if not all([URI, USERNAME, PASSWORD]):
    raise RuntimeError(
        "Missing COGNODB_URI, COGNODB_USERNAME, or COGNODB_PASSWORD"
    )


def main():
    schema_path = Path(__file__).parent.parent / "database" / "schema" / "constraints.cypher"
    schema = schema_path.read_text()

    statements = [
        statement.strip()
        for statement in schema.split(";")
        if statement.strip()
    ]

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        driver.verify_connectivity()

        with driver.session() as session:
            for statement in statements:
                session.run(statement).consume()
                print(f"✓ Applied: {statement.splitlines()[0]}")

        print("\n✓ Database schema applied successfully")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
