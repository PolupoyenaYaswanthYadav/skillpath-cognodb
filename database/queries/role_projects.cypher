MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
MATCH (s)-[:DEMONSTRATED_BY]->(p:Project)
OPTIONAL MATCH (t:Technology)-[:USED_IN]->(p)
RETURN
    p.id AS project_id,
    p.name AS project_name,
    p.description AS description,
    p.difficulty AS difficulty,
    p.estimated_hours AS estimated_hours,
    collect(DISTINCT s.name) AS demonstrated_skills,
    collect(DISTINCT t.name) AS technologies
ORDER BY
    CASE p.difficulty
        WHEN 'Beginner' THEN 1
        WHEN 'Intermediate' THEN 2
        WHEN 'Advanced' THEN 3
        ELSE 4
    END,
    p.name;
