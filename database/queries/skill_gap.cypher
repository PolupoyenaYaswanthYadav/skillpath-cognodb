MATCH (source:Role {id: $source_role_id})-[:REQUIRES]->(source_skill:Skill)
MATCH (target:Role {id: $target_role_id})-[:REQUIRES]->(target_skill:Skill)
WHERE NOT (source)-[:REQUIRES]->(target_skill)
OPTIONAL MATCH (course:Course)-[:TEACHES]->(target_skill)
RETURN
    target_skill.id AS skill_id,
    target_skill.name AS skill_name,
    target_skill.category AS category,
    target_skill.difficulty AS difficulty,
    collect(DISTINCT {
        id: course.id,
        name: course.name,
        provider: course.provider,
        level: course.level
    }) AS learning_options
ORDER BY
    CASE target_skill.difficulty
        WHEN 'Beginner' THEN 1
        WHEN 'Intermediate' THEN 2
        WHEN 'Advanced' THEN 3
        ELSE 4
    END,
    target_skill.name;
