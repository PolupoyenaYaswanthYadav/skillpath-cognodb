import json
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

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def create_nodes(tx, label, records):
    query = f"""
    UNWIND $records AS item
    MERGE (n:{label} {{id: item.id}})
    SET n += item
    """
    tx.run(query, records=records).consume()


def create_relationships(tx, query, records):
    tx.run(query, records=records).consume()


def seed_nodes(session):
    datasets = [
        ("roles.json", "Role"),
        ("skills.json", "Skill"),
        ("technologies.json", "Technology"),
        ("projects.json", "Project"),
        ("companies.json", "Company"),
        ("courses.json", "Course"),
    ]

    for filename, label in datasets:
        records = load_json(filename)

        session.execute_write(
            create_nodes,
            label,
            records,
        )

        print(f"✓ Loaded {len(records):>2} {label} nodes")


def seed_relationships(session):
    relationships = [
        (
            "Role → Skill",
            """
            UNWIND $records AS item
            MATCH (r:Role {id: item.role_id})
            MATCH (s:Skill {id: item.skill_id})
            MERGE (r)-[rel:REQUIRES]->(s)
            SET rel.importance = item.importance
            """,
            ROLE_SKILLS,
        ),
        (
            "Role → Technology",
            """
            UNWIND $records AS item
            MATCH (r:Role {id: item.role_id})
            MATCH (t:Technology {id: item.technology_id})
            MERGE (r)-[rel:USES]->(t)
            SET rel.importance = item.importance
            """,
            ROLE_TECHNOLOGIES,
        ),
        (
            "Skill → Skill",
            """
            UNWIND $records AS item
            MATCH (a:Skill {id: item.from_skill})
            MATCH (b:Skill {id: item.to_skill})
            MERGE (a)-[:PREREQUISITE_OF]->(b)
            """,
            SKILL_PREREQUISITES,
        ),
        (
            "Skill → Project",
            """
            UNWIND $records AS item
            MATCH (s:Skill {id: item.skill_id})
            MATCH (p:Project {id: item.project_id})
            MERGE (s)-[:DEMONSTRATED_BY]->(p)
            """,
            SKILL_PROJECTS,
        ),
        (
            "Technology → Project",
            """
            UNWIND $records AS item
            MATCH (t:Technology {id: item.technology_id})
            MATCH (p:Project {id: item.project_id})
            MERGE (t)-[:USED_IN]->(p)
            """,
            TECHNOLOGY_PROJECTS,
        ),
        (
            "Course → Skill",
            """
            UNWIND $records AS item
            MATCH (c:Course {id: item.course_id})
            MATCH (s:Skill {id: item.skill_id})
            MERGE (c)-[:TEACHES]->(s)
            """,
            COURSE_SKILLS,
        ),
        (
            "Course → Technology",
            """
            UNWIND $records AS item
            MATCH (c:Course {id: item.course_id})
            MATCH (t:Technology {id: item.technology_id})
            MERGE (c)-[:COVERS]->(t)
            """,
            COURSE_TECHNOLOGIES,
        ),
        (
            "Company → Role",
            """
            UNWIND $records AS item
            MATCH (c:Company {id: item.company_id})
            MATCH (r:Role {id: item.role_id})
            MERGE (c)-[:HIRES_FOR]->(r)
            """,
            COMPANY_ROLES,
        ),
        (
            "Role → Role",
            """
            UNWIND $records AS item
            MATCH (a:Role {id: item.from_role})
            MATCH (b:Role {id: item.to_role})
            MERGE (a)-[rel:SIMILAR_TO]->(b)
            SET rel.score = item.score
            """,
            ROLE_SIMILARITY,
        ),
    ]

    for name, query, records in relationships:
        session.execute_write(
            create_relationships,
            query,
            records,
        )

        print(f"✓ Created {len(records):>3} {name} relationships")


# ---------------------------------------------------------
# Relationship data
# ---------------------------------------------------------

ROLE_SKILLS = [
    {"role_id": "data-analyst", "skill_id": "sql", "importance": 5},
    {"role_id": "data-analyst", "skill_id": "statistics", "importance": 4},
    {"role_id": "data-analyst", "skill_id": "data-analysis", "importance": 5},
    {"role_id": "data-analyst", "skill_id": "data-visualization", "importance": 4},
    {"role_id": "data-analyst", "skill_id": "business-analysis", "importance": 4},
    {"role_id": "data-analyst", "skill_id": "communication", "importance": 3},
    {"role_id": "data-analyst", "skill_id": "experimentation", "importance": 3},
    {"role_id": "data-analyst", "skill_id": "python-programming", "importance": 3},

    {"role_id": "data-engineer", "skill_id": "sql", "importance": 5},
    {"role_id": "data-engineer", "skill_id": "python-programming", "importance": 5},
    {"role_id": "data-engineer", "skill_id": "data-modeling", "importance": 5},
    {"role_id": "data-engineer", "skill_id": "etl-design", "importance": 5},
    {"role_id": "data-engineer", "skill_id": "data-pipelines", "importance": 5},
    {"role_id": "data-engineer", "skill_id": "distributed-systems", "importance": 4},
    {"role_id": "data-engineer", "skill_id": "stream-processing", "importance": 4},
    {"role_id": "data-engineer", "skill_id": "data-quality", "importance": 4},
    {"role_id": "data-engineer", "skill_id": "database-design", "importance": 4},
    {"role_id": "data-engineer", "skill_id": "linux", "importance": 3},

    {"role_id": "data-scientist", "skill_id": "python-programming", "importance": 5},
    {"role_id": "data-scientist", "skill_id": "statistics", "importance": 5},
    {"role_id": "data-scientist", "skill_id": "probability", "importance": 4},
    {"role_id": "data-scientist", "skill_id": "machine-learning", "importance": 5},
    {"role_id": "data-scientist", "skill_id": "feature-engineering", "importance": 4},
    {"role_id": "data-scientist", "skill_id": "model-evaluation", "importance": 4},
    {"role_id": "data-scientist", "skill_id": "data-analysis", "importance": 4},
    {"role_id": "data-scientist", "skill_id": "sql", "importance": 3},

    {"role_id": "ml-engineer", "skill_id": "python-programming", "importance": 5},
    {"role_id": "ml-engineer", "skill_id": "machine-learning", "importance": 5},
    {"role_id": "ml-engineer", "skill_id": "deep-learning", "importance": 4},
    {"role_id": "ml-engineer", "skill_id": "model-evaluation", "importance": 4},
    {"role_id": "ml-engineer", "skill_id": "ml-deployment", "importance": 5},
    {"role_id": "ml-engineer", "skill_id": "containerization", "importance": 4},
    {"role_id": "ml-engineer", "skill_id": "software-design", "importance": 4},
    {"role_id": "ml-engineer", "skill_id": "api-development", "importance": 3},

    {"role_id": "ai-engineer", "skill_id": "python-programming", "importance": 5},
    {"role_id": "ai-engineer", "skill_id": "machine-learning", "importance": 4},
    {"role_id": "ai-engineer", "skill_id": "natural-language-processing", "importance": 4},
    {"role_id": "ai-engineer", "skill_id": "deep-learning", "importance": 4},
    {"role_id": "ai-engineer", "skill_id": "api-development", "importance": 4},
    {"role_id": "ai-engineer", "skill_id": "software-design", "importance": 4},
    {"role_id": "ai-engineer", "skill_id": "system-design", "importance": 3},

    {"role_id": "backend-engineer", "skill_id": "python-programming", "importance": 4},
    {"role_id": "backend-engineer", "skill_id": "backend-development", "importance": 5},
    {"role_id": "backend-engineer", "skill_id": "api-development", "importance": 5},
    {"role_id": "backend-engineer", "skill_id": "database-design", "importance": 4},
    {"role_id": "backend-engineer", "skill_id": "system-design", "importance": 5},
    {"role_id": "backend-engineer", "skill_id": "testing", "importance": 4},
    {"role_id": "backend-engineer", "skill_id": "object-oriented-programming", "importance": 4},
    {"role_id": "backend-engineer", "skill_id": "algorithms", "importance": 3},

    {"role_id": "software-engineer", "skill_id": "object-oriented-programming", "importance": 4},
    {"role_id": "software-engineer", "skill_id": "data-structures", "importance": 4},
    {"role_id": "software-engineer", "skill_id": "algorithms", "importance": 4},
    {"role_id": "software-engineer", "skill_id": "software-design", "importance": 5},
    {"role_id": "software-engineer", "skill_id": "testing", "importance": 4},
    {"role_id": "software-engineer", "skill_id": "git-workflows", "importance": 4},
    {"role_id": "software-engineer", "skill_id": "problem-solving", "importance": 5},

    {"role_id": "analytics-engineer", "skill_id": "sql", "importance": 5},
    {"role_id": "analytics-engineer", "skill_id": "data-modeling", "importance": 5},
    {"role_id": "analytics-engineer", "skill_id": "data-quality", "importance": 4},
    {"role_id": "analytics-engineer", "skill_id": "etl-design", "importance": 4},
    {"role_id": "analytics-engineer", "skill_id": "data-governance", "importance": 3},
    {"role_id": "analytics-engineer", "skill_id": "business-analysis", "importance": 4},
    {"role_id": "analytics-engineer", "skill_id": "python-programming", "importance": 3},

    {"role_id": "mlops-engineer", "skill_id": "python-programming", "importance": 4},
    {"role_id": "mlops-engineer", "skill_id": "ml-deployment", "importance": 5},
    {"role_id": "mlops-engineer", "skill_id": "ml-monitoring", "importance": 5},
    {"role_id": "mlops-engineer", "skill_id": "containerization", "importance": 5},
    {"role_id": "mlops-engineer", "skill_id": "ci-cd", "importance": 5},
    {"role_id": "mlops-engineer", "skill_id": "cloud-architecture", "importance": 4},
    {"role_id": "mlops-engineer", "skill_id": "infrastructure-as-code", "importance": 4},
    {"role_id": "mlops-engineer", "skill_id": "linux", "importance": 4},

    {"role_id": "cloud-engineer", "skill_id": "cloud-architecture", "importance": 5},
    {"role_id": "cloud-engineer", "skill_id": "linux", "importance": 4},
    {"role_id": "cloud-engineer", "skill_id": "networking", "importance": 4},
    {"role_id": "cloud-engineer", "skill_id": "containerization", "importance": 4},
    {"role_id": "cloud-engineer", "skill_id": "infrastructure-as-code", "importance": 5},
    {"role_id": "cloud-engineer", "skill_id": "system-design", "importance": 4},

    {"role_id": "devops-engineer", "skill_id": "linux", "importance": 5},
    {"role_id": "devops-engineer", "skill_id": "ci-cd", "importance": 5},
    {"role_id": "devops-engineer", "skill_id": "containerization", "importance": 5},
    {"role_id": "devops-engineer", "skill_id": "cloud-architecture", "importance": 4},
    {"role_id": "devops-engineer", "skill_id": "infrastructure-as-code", "importance": 5},
    {"role_id": "devops-engineer", "skill_id": "networking", "importance": 4},

    {"role_id": "bi-developer", "skill_id": "sql", "importance": 5},
    {"role_id": "bi-developer", "skill_id": "data-modeling", "importance": 4},
    {"role_id": "bi-developer", "skill_id": "data-visualization", "importance": 5},
    {"role_id": "bi-developer", "skill_id": "business-analysis", "importance": 4},
    {"role_id": "bi-developer", "skill_id": "data-analysis", "importance": 4},

    {"role_id": "nlp-engineer", "skill_id": "python-programming", "importance": 5},
    {"role_id": "nlp-engineer", "skill_id": "natural-language-processing", "importance": 5},
    {"role_id": "nlp-engineer", "skill_id": "machine-learning", "importance": 4},
    {"role_id": "nlp-engineer", "skill_id": "deep-learning", "importance": 4},
    {"role_id": "nlp-engineer", "skill_id": "model-evaluation", "importance": 3},
    {"role_id": "nlp-engineer", "skill_id": "research-methodology", "importance": 3},

    {"role_id": "computer-vision-engineer", "skill_id": "python-programming", "importance": 5},
    {"role_id": "computer-vision-engineer", "skill_id": "computer-vision", "importance": 5},
    {"role_id": "computer-vision-engineer", "skill_id": "deep-learning", "importance": 5},
    {"role_id": "computer-vision-engineer", "skill_id": "machine-learning", "importance": 4},
    {"role_id": "computer-vision-engineer", "skill_id": "model-evaluation", "importance": 4},
    {"role_id": "computer-vision-engineer", "skill_id": "research-methodology", "importance": 3},

    {"role_id": "research-engineer", "skill_id": "python-programming", "importance": 5},
    {"role_id": "research-engineer", "skill_id": "algorithms", "importance": 4},
    {"role_id": "research-engineer", "skill_id": "machine-learning", "importance": 4},
    {"role_id": "research-engineer", "skill_id": "deep-learning", "importance": 4},
    {"role_id": "research-engineer", "skill_id": "research-methodology", "importance": 5},
    {"role_id": "research-engineer", "skill_id": "linear-algebra", "importance": 4},
    {"role_id": "research-engineer", "skill_id": "optimization", "importance": 4}
]


ROLE_TECHNOLOGIES = [
    {"role_id": "data-analyst", "technology_id": "python", "importance": 4},
    {"role_id": "data-analyst", "technology_id": "pandas", "importance": 5},
    {"role_id": "data-analyst", "technology_id": "numpy", "importance": 3},
    {"role_id": "data-analyst", "technology_id": "postgresql", "importance": 4},

    {"role_id": "data-engineer", "technology_id": "python", "importance": 5},
    {"role_id": "data-engineer", "technology_id": "postgresql", "importance": 4},
    {"role_id": "data-engineer", "technology_id": "apache-spark", "importance": 5},
    {"role_id": "data-engineer", "technology_id": "apache-kafka", "importance": 4},
    {"role_id": "data-engineer", "technology_id": "apache-airflow", "importance": 5},
    {"role_id": "data-engineer", "technology_id": "dbt", "importance": 4},

    {"role_id": "data-scientist", "technology_id": "python", "importance": 5},
    {"role_id": "data-scientist", "technology_id": "pandas", "importance": 5},
    {"role_id": "data-scientist", "technology_id": "numpy", "importance": 4},
    {"role_id": "data-scientist", "technology_id": "scikit-learn", "importance": 5},
    {"role_id": "data-scientist", "technology_id": "postgresql", "importance": 3},

    {"role_id": "ml-engineer", "technology_id": "python", "importance": 5},
    {"role_id": "ml-engineer", "technology_id": "pytorch", "importance": 4},
    {"role_id": "ml-engineer", "technology_id": "scikit-learn", "importance": 4},
    {"role_id": "ml-engineer", "technology_id": "docker", "importance": 5},
    {"role_id": "ml-engineer", "technology_id": "fastapi", "importance": 4},
    {"role_id": "ml-engineer", "technology_id": "mlflow", "importance": 4},

    {"role_id": "ai-engineer", "technology_id": "python", "importance": 5},
    {"role_id": "ai-engineer", "technology_id": "pytorch", "importance": 4},
    {"role_id": "ai-engineer", "technology_id": "hugging-face", "importance": 5},
    {"role_id": "ai-engineer", "technology_id": "fastapi", "importance": 4},
    {"role_id": "ai-engineer", "technology_id": "docker", "importance": 4},

    {"role_id": "backend-engineer", "technology_id": "python", "importance": 4},
    {"role_id": "backend-engineer", "technology_id": "fastapi", "importance": 5},
    {"role_id": "backend-engineer", "technology_id": "postgresql", "importance": 5},
    {"role_id": "backend-engineer", "technology_id": "redis", "importance": 4},
    {"role_id": "backend-engineer", "technology_id": "docker", "importance": 4},

    {"role_id": "software-engineer", "technology_id": "git", "importance": 5},
    {"role_id": "software-engineer", "technology_id": "docker", "importance": 3},
    {"role_id": "software-engineer", "technology_id": "react", "importance": 3},

    {"role_id": "analytics-engineer", "technology_id": "dbt", "importance": 5},
    {"role_id": "analytics-engineer", "technology_id": "postgresql", "importance": 5},
    {"role_id": "analytics-engineer", "technology_id": "python", "importance": 3},

    {"role_id": "mlops-engineer", "technology_id": "docker", "importance": 5},
    {"role_id": "mlops-engineer", "technology_id": "kubernetes", "importance": 5},
    {"role_id": "mlops-engineer", "technology_id": "mlflow", "importance": 5},
    {"role_id": "mlops-engineer", "technology_id": "github-actions", "importance": 4},
    {"role_id": "mlops-engineer", "technology_id": "terraform", "importance": 4},
    {"role_id": "mlops-engineer", "technology_id": "aws", "importance": 4},

    {"role_id": "cloud-engineer", "technology_id": "aws", "importance": 5},
    {"role_id": "cloud-engineer", "technology_id": "terraform", "importance": 5},
    {"role_id": "cloud-engineer", "technology_id": "kubernetes", "importance": 4},
    {"role_id": "cloud-engineer", "technology_id": "docker", "importance": 4},

    {"role_id": "devops-engineer", "technology_id": "docker", "importance": 5},
    {"role_id": "devops-engineer", "technology_id": "kubernetes", "importance": 5},
    {"role_id": "devops-engineer", "technology_id": "github-actions", "importance": 5},
    {"role_id": "devops-engineer", "technology_id": "terraform", "importance": 5},
    {"role_id": "devops-engineer", "technology_id": "aws", "importance": 4},

    {"role_id": "bi-developer", "technology_id": "postgresql", "importance": 5},
    {"role_id": "bi-developer", "technology_id": "pandas", "importance": 3},

    {"role_id": "nlp-engineer", "technology_id": "python", "importance": 5},
    {"role_id": "nlp-engineer", "technology_id": "pytorch", "importance": 5},
    {"role_id": "nlp-engineer", "technology_id": "hugging-face", "importance": 5},

    {"role_id": "computer-vision-engineer", "technology_id": "python", "importance": 5},
    {"role_id": "computer-vision-engineer", "technology_id": "pytorch", "importance": 5},
    {"role_id": "computer-vision-engineer", "technology_id": "tensorflow", "importance": 4},

    {"role_id": "research-engineer", "technology_id": "python", "importance": 5},
    {"role_id": "research-engineer", "technology_id": "pytorch", "importance": 5},
    {"role_id": "research-engineer", "technology_id": "tensorflow", "importance": 4}
]


SKILL_PREREQUISITES = [
    {"from_skill": "sql", "to_skill": "data-modeling"},
    {"from_skill": "data-analysis", "to_skill": "machine-learning"},
    {"from_skill": "statistics", "to_skill": "machine-learning"},
    {"from_skill": "probability", "to_skill": "statistics"},
    {"from_skill": "linear-algebra", "to_skill": "deep-learning"},
    {"from_skill": "machine-learning", "to_skill": "deep-learning"},
    {"from_skill": "machine-learning", "to_skill": "ml-deployment"},
    {"from_skill": "backend-development", "to_skill": "system-design"},
    {"from_skill": "containerization", "to_skill": "ci-cd"},
    {"from_skill": "cloud-architecture", "to_skill": "infrastructure-as-code"},
    {"from_skill": "data-modeling", "to_skill": "data-pipelines"},
    {"from_skill": "etl-design", "to_skill": "data-pipelines"},
    {"from_skill": "data-pipelines", "to_skill": "distributed-systems"},
    {"from_skill": "natural-language-processing", "to_skill": "deep-learning"},
    {"from_skill": "computer-vision", "to_skill": "deep-learning"},
    {"from_skill": "deep-learning", "to_skill": "model-evaluation"},
    {"from_skill": "python-programming", "to_skill": "machine-learning"},
    {"from_skill": "python-programming", "to_skill": "backend-development"},
    {"from_skill": "data-structures", "to_skill": "algorithms"}
]


SKILL_PROJECTS = [
    {"skill_id": "sql", "project_id": "etl-pipeline"},
    {"skill_id": "data-modeling", "project_id": "etl-pipeline"},
    {"skill_id": "etl-design", "project_id": "etl-pipeline"},
    {"skill_id": "data-pipelines", "project_id": "etl-pipeline"},
    {"skill_id": "sql", "project_id": "data-warehouse"},
    {"skill_id": "data-modeling", "project_id": "data-warehouse"},
    {"skill_id": "data-governance", "project_id": "data-warehouse"},
    {"skill_id": "stream-processing", "project_id": "streaming-analytics"},
    {"skill_id": "distributed-systems", "project_id": "streaming-analytics"},
    {"skill_id": "data-pipelines", "project_id": "streaming-analytics"},
    {"skill_id": "machine-learning", "project_id": "fraud-detection"},
    {"skill_id": "feature-engineering", "project_id": "fraud-detection"},
    {"skill_id": "model-evaluation", "project_id": "fraud-detection"},
    {"skill_id": "statistics", "project_id": "fraud-detection"},
    {"skill_id": "machine-learning", "project_id": "customer-churn"},
    {"skill_id": "statistics", "project_id": "customer-churn"},
    {"skill_id": "feature-engineering", "project_id": "customer-churn"},
    {"skill_id": "machine-learning", "project_id": "recommendation-engine"},
    {"skill_id": "deep-learning", "project_id": "recommendation-engine"},
    {"skill_id": "machine-learning", "project_id": "customer-segmentation"},
    {"skill_id": "statistics", "project_id": "customer-segmentation"},
    {"skill_id": "data-visualization", "project_id": "sales-dashboard"},
    {"skill_id": "data-analysis", "project_id": "sales-dashboard"},
    {"skill_id": "api-development", "project_id": "ml-api"},
    {"skill_id": "machine-learning", "project_id": "ml-api"},
    {"skill_id": "ml-deployment", "project_id": "ml-platform"},
    {"skill_id": "ml-monitoring", "project_id": "ml-platform"},
    {"skill_id": "ci-cd", "project_id": "ml-platform"},
    {"skill_id": "containerization", "project_id": "ml-platform"},
    {"skill_id": "data-quality", "project_id": "data-quality"},
    {"skill_id": "data-pipelines", "project_id": "data-quality"},
    {"skill_id": "distributed-systems", "project_id": "event-platform"},
    {"skill_id": "stream-processing", "project_id": "event-platform"},
    {"skill_id": "api-development", "project_id": "api-platform"},
    {"skill_id": "system-design", "project_id": "api-platform"},
    {"skill_id": "data-modeling", "project_id": "analytics-model"},
    {"skill_id": "sql", "project_id": "analytics-model"},
    {"skill_id": "data-quality", "project_id": "analytics-model"},
    {"skill_id": "natural-language-processing", "project_id": "nlp-classifier"},
    {"skill_id": "machine-learning", "project_id": "nlp-classifier"},
    {"skill_id": "computer-vision", "project_id": "vision-inspection"},
    {"skill_id": "deep-learning", "project_id": "vision-inspection"},
    {"skill_id": "cloud-architecture", "project_id": "cloud-data-lake"},
    {"skill_id": "data-pipelines", "project_id": "cloud-data-lake"},
    {"skill_id": "ci-cd", "project_id": "ci-cd-platform"},
    {"skill_id": "software-design", "project_id": "ci-cd-platform"},
    {"skill_id": "research-methodology", "project_id": "experiment-platform"},
    {"skill_id": "statistics", "project_id": "experiment-platform"},
    {"skill_id": "natural-language-processing", "project_id": "search-engine"},
    {"skill_id": "machine-learning", "project_id": "search-engine"},
    {"skill_id": "data-pipelines", "project_id": "data-migration"},
    {"skill_id": "data-quality", "project_id": "data-migration"},
    {"skill_id": "machine-learning", "project_id": "time-series-forecasting"},
    {"skill_id": "statistics", "project_id": "time-series-forecasting"}
]


TECHNOLOGY_PROJECTS = [
    {"technology_id": "python", "project_id": "etl-pipeline"},
    {"technology_id": "postgresql", "project_id": "etl-pipeline"},
    {"technology_id": "apache-airflow", "project_id": "etl-pipeline"},
    {"technology_id": "python", "project_id": "streaming-analytics"},
    {"technology_id": "apache-kafka", "project_id": "streaming-analytics"},
    {"technology_id": "apache-spark", "project_id": "streaming-analytics"},
    {"technology_id": "python", "project_id": "fraud-detection"},
    {"technology_id": "pandas", "project_id": "fraud-detection"},
    {"technology_id": "scikit-learn", "project_id": "fraud-detection"},
    {"technology_id": "python", "project_id": "customer-churn"},
    {"technology_id": "pandas", "project_id": "customer-churn"},
    {"technology_id": "scikit-learn", "project_id": "customer-churn"},
    {"technology_id": "python", "project_id": "recommendation-engine"},
    {"technology_id": "pytorch", "project_id": "recommendation-engine"},
    {"technology_id": "python", "project_id": "data-warehouse"},
    {"technology_id": "postgresql", "project_id": "data-warehouse"},
    {"technology_id": "dbt", "project_id": "data-warehouse"},
    {"technology_id": "postgresql", "project_id": "sales-dashboard"},
    {"technology_id": "pandas", "project_id": "sales-dashboard"},
    {"technology_id": "python", "project_id": "customer-segmentation"},
    {"technology_id": "pandas", "project_id": "customer-segmentation"},
    {"technology_id": "scikit-learn", "project_id": "customer-segmentation"},
    {"technology_id": "fastapi", "project_id": "ml-api"},
    {"technology_id": "scikit-learn", "project_id": "ml-api"},
    {"technology_id": "docker", "project_id": "ml-api"},
    {"technology_id": "mlflow", "project_id": "ml-platform"},
    {"technology_id": "docker", "project_id": "ml-platform"},
    {"technology_id": "kubernetes", "project_id": "ml-platform"},
    {"technology_id": "github-actions", "project_id": "ml-platform"},
    {"technology_id": "python", "project_id": "data-quality"},
    {"technology_id": "pandas", "project_id": "data-quality"},
    {"technology_id": "apache-kafka", "project_id": "event-platform"},
    {"technology_id": "apache-spark", "project_id": "event-platform"},
    {"technology_id": "fastapi", "project_id": "api-platform"},
    {"technology_id": "postgresql", "project_id": "api-platform"},
    {"technology_id": "redis", "project_id": "api-platform"},
    {"technology_id": "dbt", "project_id": "analytics-model"},
    {"technology_id": "postgresql", "project_id": "analytics-model"},
    {"technology_id": "python", "project_id": "nlp-classifier"},
    {"technology_id": "pytorch", "project_id": "nlp-classifier"},
    {"technology_id": "hugging-face", "project_id": "nlp-classifier"},
    {"technology_id": "python", "project_id": "vision-inspection"},
    {"technology_id": "pytorch", "project_id": "vision-inspection"},
    {"technology_id": "tensorflow", "project_id": "vision-inspection"},
    {"technology_id": "aws", "project_id": "cloud-data-lake"},
    {"technology_id": "apache-spark", "project_id": "cloud-data-lake"},
    {"technology_id": "docker", "project_id": "ci-cd-platform"},
    {"technology_id": "github-actions", "project_id": "ci-cd-platform"},
    {"technology_id": "python", "project_id": "experiment-platform"},
    {"technology_id": "postgresql", "project_id": "data-migration"},
    {"technology_id": "aws", "project_id": "data-migration"},
    {"technology_id": "python", "project_id": "time-series-forecasting"},
    {"technology_id": "pandas", "project_id": "time-series-forecasting"},
    {"technology_id": "scikit-learn", "project_id": "time-series-forecasting"},
    {"technology_id": "hugging-face", "project_id": "search-engine"},
    {"technology_id": "python", "project_id": "search-engine"}
]


COURSE_SKILLS = [
    {"course_id": "sql-data-analysis", "skill_id": "sql"},
    {"course_id": "sql-data-analysis", "skill_id": "data-analysis"},
    {"course_id": "python-data-science", "skill_id": "python-programming"},
    {"course_id": "python-data-science", "skill_id": "data-analysis"},
    {"course_id": "data-engineering", "skill_id": "data-pipelines"},
    {"course_id": "data-engineering", "skill_id": "data-modeling"},
    {"course_id": "spark-processing", "skill_id": "distributed-systems"},
    {"course_id": "spark-processing", "skill_id": "data-pipelines"},
    {"course_id": "airflow-orchestration", "skill_id": "etl-design"},
    {"course_id": "airflow-orchestration", "skill_id": "data-pipelines"},
    {"course_id": "machine-learning", "skill_id": "machine-learning"},
    {"course_id": "machine-learning", "skill_id": "model-evaluation"},
    {"course_id": "deep-learning", "skill_id": "deep-learning"},
    {"course_id": "deep-learning", "skill_id": "linear-algebra"},
    {"course_id": "mlops", "skill_id": "ml-deployment"},
    {"course_id": "mlops", "skill_id": "ml-monitoring"},
    {"course_id": "docker-course", "skill_id": "containerization"},
    {"course_id": "kubernetes-course", "skill_id": "containerization"},
    {"course_id": "kubernetes-course", "skill_id": "cloud-architecture"},
    {"course_id": "aws-cloud", "skill_id": "cloud-architecture"},
    {"course_id": "system-design", "skill_id": "system-design"},
    {"course_id": "statistics-course", "skill_id": "statistics"},
    {"course_id": "statistics-course", "skill_id": "probability"},
    {"course_id": "nlp-course", "skill_id": "natural-language-processing"},
    {"course_id": "computer-vision-course", "skill_id": "computer-vision"},
    {"course_id": "postgres-course", "skill_id": "database-design"},
    {"course_id": "dbt-course", "skill_id": "data-modeling"},
    {"course_id": "dbt-course", "skill_id": "data-quality"},
    {"course_id": "kafka-course", "skill_id": "stream-processing"},
    {"course_id": "terraform-course", "skill_id": "infrastructure-as-code"},
    {"course_id": "git-course", "skill_id": "git-workflows"}
]


COURSE_TECHNOLOGIES = [
    {"course_id": "sql-data-analysis", "technology_id": "postgresql"},
    {"course_id": "python-data-science", "technology_id": "python"},
    {"course_id": "python-data-science", "technology_id": "pandas"},
    {"course_id": "data-engineering", "technology_id": "apache-spark"},
    {"course_id": "data-engineering", "technology_id": "dbt"},
    {"course_id": "spark-processing", "technology_id": "apache-spark"},
    {"course_id": "airflow-orchestration", "technology_id": "apache-airflow"},
    {"course_id": "machine-learning", "technology_id": "scikit-learn"},
    {"course_id": "deep-learning", "technology_id": "pytorch"},
    {"course_id": "mlops", "technology_id": "mlflow"},
    {"course_id": "mlops", "technology_id": "docker"},
    {"course_id": "docker-course", "technology_id": "docker"},
    {"course_id": "kubernetes-course", "technology_id": "kubernetes"},
    {"course_id": "aws-cloud", "technology_id": "aws"},
    {"course_id": "system-design", "technology_id": "redis"},
    {"course_id": "nlp-course", "technology_id": "hugging-face"},
    {"course_id": "computer-vision-course", "technology_id": "pytorch"},
    {"course_id": "postgres-course", "technology_id": "postgresql"},
    {"course_id": "dbt-course", "technology_id": "dbt"},
    {"course_id": "kafka-course", "technology_id": "apache-kafka"},
    {"course_id": "terraform-course", "technology_id": "terraform"},
    {"course_id": "git-course", "technology_id": "git"},
    {"course_id": "git-course", "technology_id": "github-actions"}
]


COMPANY_ROLES = [
    {"company_id": "google", "role_id": "software-engineer"},
    {"company_id": "google", "role_id": "data-scientist"},
    {"company_id": "google", "role_id": "ml-engineer"},
    {"company_id": "google", "role_id": "ai-engineer"},
    {"company_id": "microsoft", "role_id": "software-engineer"},
    {"company_id": "microsoft", "role_id": "data-engineer"},
    {"company_id": "microsoft", "role_id": "ai-engineer"},
    {"company_id": "amazon", "role_id": "software-engineer"},
    {"company_id": "amazon", "role_id": "data-engineer"},
    {"company_id": "amazon", "role_id": "cloud-engineer"},
    {"company_id": "meta", "role_id": "software-engineer"},
    {"company_id": "meta", "role_id": "ml-engineer"},
    {"company_id": "meta", "role_id": "research-engineer"},
    {"company_id": "netflix", "role_id": "data-scientist"},
    {"company_id": "netflix", "role_id": "data-engineer"},
    {"company_id": "uber", "role_id": "data-scientist"},
    {"company_id": "uber", "role_id": "data-engineer"},
    {"company_id": "uber", "role_id": "ml-engineer"},
    {"company_id": "databricks", "role_id": "data-engineer"},
    {"company_id": "databricks", "role_id": "ml-engineer"},
    {"company_id": "databricks", "role_id": "research-engineer"},
    {"company_id": "snowflake", "role_id": "data-engineer"},
    {"company_id": "snowflake", "role_id": "analytics-engineer"},
    {"company_id": "atlassian", "role_id": "software-engineer"},
    {"company_id": "atlassian", "role_id": "backend-engineer"},
    {"company_id": "adobe", "role_id": "data-scientist"},
    {"company_id": "adobe", "role_id": "ml-engineer"},
    {"company_id": "flipkart", "role_id": "data-scientist"},
    {"company_id": "flipkart", "role_id": "data-engineer"},
    {"company_id": "razorpay", "role_id": "backend-engineer"},
    {"company_id": "razorpay", "role_id": "data-engineer"},
    {"company_id": "swiggy", "role_id": "data-scientist"},
    {"company_id": "swiggy", "role_id": "data-engineer"},
    {"company_id": "phonepe", "role_id": "backend-engineer"},
    {"company_id": "phonepe", "role_id": "data-scientist"},
    {"company_id": "zomato", "role_id": "data-scientist"},
    {"company_id": "zomato", "role_id": "data-engineer"},
    {"company_id": "salesforce", "role_id": "software-engineer"},
    {"company_id": "salesforce", "role_id": "data-scientist"},
    {"company_id": "airbnb", "role_id": "data-scientist"},
    {"company_id": "airbnb", "role_id": "data-engineer"},
    {"company_id": "linkedin", "role_id": "data-scientist"},
    {"company_id": "linkedin", "role_id": "ml-engineer"},
    {"company_id": "nvidia", "role_id": "ml-engineer"},
    {"company_id": "nvidia", "role_id": "research-engineer"},
    {"company_id": "stripe", "role_id": "backend-engineer"},
    {"company_id": "stripe", "role_id": "data-scientist"}
]


ROLE_SIMILARITY = [
    {"from_role": "data-analyst", "to_role": "analytics-engineer", "score": 0.88},
    {"from_role": "data-analyst", "to_role": "data-scientist", "score": 0.76},
    {"from_role": "data-analyst", "to_role": "bi-developer", "score": 0.84},
    {"from_role": "analytics-engineer", "to_role": "data-engineer", "score": 0.86},
    {"from_role": "analytics-engineer", "to_role": "data-analyst", "score": 0.88},
    {"from_role": "data-engineer", "to_role": "analytics-engineer", "score": 0.86},
    {"from_role": "data-engineer", "to_role": "backend-engineer", "score": 0.67},
    {"from_role": "data-engineer", "to_role": "data-scientist", "score": 0.62},
    {"from_role": "data-scientist", "to_role": "ml-engineer", "score": 0.84},
    {"from_role": "data-scientist", "to_role": "research-engineer", "score": 0.78},
    {"from_role": "data-scientist", "to_role": "data-analyst", "score": 0.76},
    {"from_role": "ml-engineer", "to_role": "ai-engineer", "score": 0.91},
    {"from_role": "ml-engineer", "to_role": "mlops-engineer", "score": 0.82},
    {"from_role": "ml-engineer", "to_role": "research-engineer", "score": 0.79},
    {"from_role": "ai-engineer", "to_role": "backend-engineer", "score": 0.74},
    {"from_role": "ai-engineer", "to_role": "nlp-engineer", "score": 0.86},
    {"from_role": "backend-engineer", "to_role": "software-engineer", "score": 0.89},
    {"from_role": "backend-engineer", "to_role": "cloud-engineer", "score": 0.72},
    {"from_role": "software-engineer", "to_role": "backend-engineer", "score": 0.89},
    {"from_role": "software-engineer", "to_role": "devops-engineer", "score": 0.69},
    {"from_role": "cloud-engineer", "to_role": "devops-engineer", "score": 0.87},
    {"from_role": "devops-engineer", "to_role": "mlops-engineer", "score": 0.73},
    {"from_role": "nlp-engineer", "to_role": "ai-engineer", "score": 0.86},
    {"from_role": "computer-vision-engineer", "to_role": "ml-engineer", "score": 0.83},
    {"from_role": "research-engineer", "to_role": "ml-engineer", "score": 0.79}
]


def main():
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        driver.verify_connectivity()

        with driver.session() as session:
            print("\n=== Loading Nodes ===\n")
            seed_nodes(session)

            print("\n=== Creating Relationships ===\n")
            seed_relationships(session)

        print("\n✓ SkillPath graph seeded successfully")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
