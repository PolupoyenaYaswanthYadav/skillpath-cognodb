import { ArrowUpRight } from "lucide-react";

export default function RoleCard({ role, onClick }) {
  return (
    <button className="role-card" onClick={() => onClick(role.id)}>
      <div>
        <span className="eyebrow">{role.category}</span>
        <h3>{role.name}</h3>
        <p>{role.seniority}</p>
      </div>
      <ArrowUpRight size={19} />
    </button>
  );
}
