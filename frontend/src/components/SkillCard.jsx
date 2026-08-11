export default function SkillCard({ skill }) {
  return (
    <div className="skill-card">
      <div>
        <strong>{skill.name}</strong>
        <span>{skill.category}</span>
      </div>

      {skill.importance && (
        <div className="importance">
          {"●".repeat(Math.min(skill.importance, 5))}
        </div>
      )}
    </div>
  );
}
