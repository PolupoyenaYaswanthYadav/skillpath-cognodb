MATCH (r:Role {id: $role_id})
OPTIONAL MATCH (r)-[req:REQUIRES]->(s:Skill)
OPTIONAL MATCH (r)-[use:USES]->(t:Technology)
RETURN
    r.id AS role_id,
    r.name AS role_name,
    r.description AS description,
    r.category AS category,
    r.seniority AS seniority,
    collect(DISTINCT {
        id: s.id,
        name: s.name,
        category: s.category,
        difficulty: s.difficulty,
        importance: req.importance
    }) AS skills,
    collect(DISTINCT {
        id: t.id,
        name: t.name,
        category: t.category,
        importance: use.importance
    }) AS technologies;
