import { Clock3, Code2 } from "lucide-react";

export default function ProjectCard({ project }) {
  return (
    <article className="project-card">
      <div className="card-topline">
        <span className={`difficulty ${project.difficulty?.toLowerCase()}`}>
          {project.difficulty}
        </span>
        <span className="hours">
          <Clock3 size={14} />
          {project.estimated_hours}h
        </span>
      </div>

      <h3>{project.project_name}</h3>
      <p>{project.description}</p>

      {project.technologies?.length > 0 && (
        <div className="tag-list">
          <Code2 size={15} />
          {project.technologies.slice(0, 4).map((technology) => (
            <span className="tag" key={technology}>
              {technology}
            </span>
          ))}
        </div>
      )}
    </article>
  );
}
