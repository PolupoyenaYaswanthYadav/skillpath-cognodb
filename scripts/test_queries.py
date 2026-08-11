import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

BASE_DIR = Path(__file__).resolve().parent.parent
QUERY_DIR = BASE_DIR / "database" / "queries"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD),
)

TESTS = {
    "role_overview.cypher": {
        "role_id": "data-engineer",
    },
    "role_projects.cypher": {
        "role_id": "data-engineer",
    },
    "skill_gap.cypher": {
        "source_role_id": "data-analyst",
        "target_role_id": "data-engineer",
    },
    "learning_path.cypher": {
        "role_id": "data-engineer",
    },
    "similar_roles.cypher": {
        "role_id": "data-engineer",
        "limit": 5,
    },
}


def main():
    with driver.session() as session:
        for filename, params in TESTS.items():
            print(f"\n=== {filename} ===")

            query = (QUERY_DIR / filename).read_text()

            try:
                records = list(session.run(query, **params))
                print(f"✓ Query executed successfully")
                print(f"  Rows returned: {len(records)}")

                if records:
                    print(f"  Sample: {records[0]}")

            except Exception as exc:
                print(f"✗ Query failed")
                print(f"  {type(exc).__name__}: {exc}")

    driver.close()


if __name__ == "__main__":
    main()
