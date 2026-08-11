import { useEffect, useState } from "react";

import Header from "./components/Header";
import Home from "./pages/Home";
import RoleDetail from "./pages/RoleDetail";
import { api } from "./services/api";

export default function App() {
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);
  const [search, setSearch] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRoles() {
      try {
        const data = await api.getRoles();
        setRoles(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadRoles();
  }, []);

  async function handleSearch(event) {
    event?.preventDefault();

    if (!search.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const results = await api.search(search.trim());
      setSearchResults(results);
    } catch (err) {
      setError(err.message);
    }
  }

  function handleRoleSelect(roleId) {
    setSearchResults([]);
    setSearch("");
    setSelectedRole(roleId);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  return (
    <div className="app">
      <Header
        search={search}
        setSearch={setSearch}
        onSearch={handleSearch}
      />

      {error && (
        <div className="global-error">
          <strong>Connection issue:</strong> {error}
        </div>
      )}

      {searchResults.length > 0 && (
        <div className="search-results">
          <div className="search-results-inner">
            <span className="eyebrow">Search results</span>

            {searchResults.map((result) => (
              <button
                key={`${result.type}-${result.id}`}
                onClick={() =>
                  result.type === "Role"
                    ? handleRoleSelect(result.id)
                    : setSearch(result.name)
                }
              >
                <div>
                  <strong>{result.name}</strong>
                  <span>{result.type}</span>
                </div>
                <span>{result.category}</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedRole ? (
        <RoleDetail
          roleId={selectedRole}
          onBack={() => setSelectedRole(null)}
          onRoleSelect={handleRoleSelect}
        />
      ) : (
        <Home
          roles={roles}
          loading={loading}
          onRoleSelect={handleRoleSelect}
        />
      )}

      <footer className="footer">
        <span>SkillPath</span>
        <span>Powered by a connected career graph</span>
      </footer>
    </div>
  );
}
