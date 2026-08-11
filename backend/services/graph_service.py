from pathlib import Path
from typing import Any

from backend.database import db


QUERY_DIR = Path(__file__).resolve().parents[2] / "database" / "queries"


def load_query(filename: str) -> str:
    return (QUERY_DIR / filename).read_text(encoding="utf-8")


def get_roles() -> list[dict[str, Any]]:
    query = """
    MATCH (r:Role)
    RETURN
        r.id AS id,
        r.name AS name,
        r.category AS category,
        r.seniority AS seniority
    ORDER BY r.name
    """

    return db.execute(query)


def get_role(role_id: str) -> list[dict[str, Any]]:
    return db.execute(
        load_query("role_overview.cypher"),
        role_id=role_id,
    )


def get_role_projects(role_id: str) -> list[dict[str, Any]]:
    return db.execute(
        load_query("role_projects.cypher"),
        role_id=role_id,
    )


def get_learning_path(role_id: str) -> list[dict[str, Any]]:
    return db.execute(
        load_query("learning_path.cypher"),
        role_id=role_id,
    )


def get_similar_roles(
    role_id: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    return db.execute(
        load_query("similar_roles.cypher"),
        role_id=role_id,
        limit=limit,
    )


def get_skill_gap(
    source_role_id: str,
    target_role_id: str,
) -> list[dict[str, Any]]:
    return db.execute(
        load_query("skill_gap.cypher"),
        source_role_id=source_role_id,
        target_role_id=target_role_id,
    )


def search_graph(search_term: str) -> list[dict[str, Any]]:
    query = """
    CALL {
        MATCH (r:Role)
        WHERE toLower(r.name) CONTAINS toLower($search_term)
        RETURN r.id AS id, r.name AS name,
               'Role' AS type, r.category AS category

        UNION ALL

        MATCH (s:Skill)
        WHERE toLower(s.name) CONTAINS toLower($search_term)
        RETURN s.id AS id, s.name AS name,
               'Skill' AS type, s.category AS category

        UNION ALL

        MATCH (t:Technology)
        WHERE toLower(t.name) CONTAINS toLower($search_term)
        RETURN t.id AS id, t.name AS name,
               'Technology' AS type, t.category AS category

        UNION ALL

        MATCH (p:Project)
        WHERE toLower(p.name) CONTAINS toLower($search_term)
        RETURN p.id AS id, p.name AS name,
               'Project' AS type, NULL AS category

        UNION ALL

        MATCH (c:Course)
        WHERE toLower(c.name) CONTAINS toLower($search_term)
        RETURN c.id AS id, c.name AS name,
               'Course' AS type, NULL AS category
    }

    RETURN id, name, type, category
    ORDER BY type, name
    LIMIT 30
    """

    return db.execute(
        query,
        search_term=search_term,
    )
