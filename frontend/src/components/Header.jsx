import { Search, Network } from "lucide-react";

export default function Header({ search, setSearch, onSearch }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="brand">
          <div className="brand-mark">
            <Network size={20} />
          </div>
          <div>
            <div className="brand-name">SkillPath</div>
            <div className="brand-tagline">Explore connected career paths</div>
          </div>
        </div>

        <form className="search-box" onSubmit={onSearch}>
          <Search size={18} />
          <input
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search roles, skills, technologies..."
            aria-label="Search"
          />
        </form>
      </div>
    </header>
  );
}
