MATCH (r:Role {id: $role_id})-[sim:SIMILAR_TO]->(similar:Role)
RETURN
    similar.id AS role_id,
    similar.name AS role_name,
    similar.description AS description,
    similar.category AS category,
    similar.seniority AS seniority,
    sim.score AS similarity_score
ORDER BY similarity_score DESC
LIMIT $limit;
