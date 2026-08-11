import { ArrowRight, Compass, GitBranch, Sparkles } from "lucide-react";
import RoleCard from "../components/RoleCard";

const featuredRoles = [
  "data-engineer",
  "data-scientist",
  "ml-engineer",
  "ai-engineer",
  "backend-engineer",
  "analytics-engineer",
];

export default function Home({ roles, loading, onRoleSelect }) {
  const featured = roles.filter((role) => featuredRoles.includes(role.id));

  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <span className="hero-label">
            <Sparkles size={15} />
            Graph-powered career exploration
          </span>

          <h1>
            Find the path between
            <span> where you are and where you want to go.</span>
          </h1>

          <p>
            Explore the relationships between roles, skills, technologies,
            projects, and learning resources in one connected graph.
          </p>
        </div>

        <div className="hero-stat">
          <GitBranch size={24} />
          <strong>Connected</strong>
          <span>career intelligence</span>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">Explore</span>
            <h2>Popular career paths</h2>
          </div>

          <span className="result-count">{roles.length} roles</span>
        </div>

        {loading ? (
          <div className="state-card">Loading roles...</div>
        ) : (
          <div className="role-grid">
            {featured.map((role) => (
              <RoleCard
                key={role.id}
                role={role}
                onClick={onRoleSelect}
              />
            ))}
          </div>
        )}
      </section>

      <section className="why-section">
        <div>
          <span className="eyebrow">Why SkillPath?</span>
          <h2>Career decisions are connected problems.</h2>
        </div>

        <div className="why-grid">
          <div>
            <Compass size={20} />
            <h3>Explore relationships</h3>
            <p>
              See how roles connect to skills, projects, technologies, and
              learning resources.
            </p>
          </div>

          <div>
            <ArrowRight size={20} />
            <h3>Find skill gaps</h3>
            <p>
              Compare career paths and identify the capabilities needed to
              move toward another role.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
