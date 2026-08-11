import { useEffect, useState } from "react";
import { ArrowLeft, Network, Target, Wrench } from "lucide-react";

import { api } from "../services/api";
import SkillCard from "../components/SkillCard";
import ProjectCard from "../components/ProjectCard";
import CourseCard from "../components/CourseCard";
import GraphView from "../components/GraphView";

export default function RoleDetail({ roleId, onBack, onRoleSelect }) {
  const [role, setRole] = useState(null);
  const [projects, setProjects] = useState([]);
  const [learning, setLearning] = useState([]);
  const [similar, setSimilar] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError("");

        const [roleData, projectData, learningData, similarData] =
          await Promise.all([
            api.getRole(roleId),
            api.getProjects(roleId),
            api.getLearningPath(roleId),
            api.getSimilarRoles(roleId),
          ]);

        setRole(roleData);
        setProjects(projectData);
        setLearning(learningData);
        setSimilar(similarData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [roleId]);

  if (loading) {
    return <main className="page-state">Loading role...</main>;
  }

  if (error) {
    return (
      <main className="page-state error-state">
        <h2>We couldn't load this role.</h2>
        <p>{error}</p>
        <button className="button" onClick={onBack}>
          Go back
        </button>
      </main>
    );
  }

  if (!role) {
    return <main className="page-state">Role not found.</main>;
  }

  return (
    <main className="detail-page">
      <button className="back-button" onClick={onBack}>
        <ArrowLeft size={17} />
        All roles
      </button>

      <section className="role-hero">
        <div>
          <span className="eyebrow">{role.category}</span>
          <h1>{role.role_name}</h1>
          <p>{role.description}</p>

          <div className="role-meta">
            <span>{role.seniority}</span>
            <span>{role.skills.length} connected skills</span>
            <span>{role.technologies.length} technologies</span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Graph view</span>
            <h2>How this role connects</h2>
          </div>
          <Network size={22} />
        </div>

        <GraphView
          role={role}
          skills={role.skills}
          technologies={role.technologies}
        />
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Core capabilities</span>
            <h2>Skills required</h2>
          </div>
          <Target size={22} />
        </div>

        <div className="skill-grid">
          {role.skills
            .filter((skill) => skill.id)
            .map((skill) => (
              <SkillCard key={skill.id} skill={skill} />
            ))}
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Build evidence</span>
            <h2>Projects to practice</h2>
          </div>
        </div>

        <div className="project-grid">
          {projects.slice(0, 6).map((project) => (
            <ProjectCard key={project.project_id} project={project} />
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Keep learning</span>
            <h2>Recommended courses</h2>
          </div>
        </div>

        <div className="course-grid">
          {learning.slice(0, 8).flatMap((item) =>
            (item.courses || [])
              .filter((course) => course.id)
              .map((course) => (
                <CourseCard
                  key={`${item.skill_id}-${course.id}`}
                  course={course}
                />
              ))
          )}
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Nearby paths</span>
            <h2>Similar roles</h2>
          </div>
        </div>

        <div className="similar-grid">
          {similar.map((item) => (
            <button
              className="similar-card"
              key={item.role_id}
              onClick={() => onRoleSelect(item.role_id)}
            >
              <div>
                <strong>{item.role_name}</strong>
                <span>{item.seniority}</span>
              </div>
              <span>{Math.round(item.similarity_score * 100)}%</span>
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}
