MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
MATCH (c:Course)-[:TEACHES]->(s)
OPTIONAL MATCH (c)-[:COVERS]->(t:Technology)
RETURN
    s.id AS skill_id,
    s.name AS skill_name,
    s.difficulty AS difficulty,
    collect(DISTINCT {
        id: c.id,
        name: c.name,
        provider: c.provider,
        level: c.level,
        technologies: CASE
            WHEN t IS NULL THEN []
            ELSE [t.name]
        END
    }) AS courses
ORDER BY
    CASE s.difficulty
        WHEN 'Beginner' THEN 1
        WHEN 'Intermediate' THEN 2
        WHEN 'Advanced' THEN 3
        ELSE 4
    END,
    s.name;
