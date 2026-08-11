const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    let message = "Something went wrong while contacting the server.";

    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {
      // Keep the fallback message.
    }

    throw new Error(message);
  }

  return response.json();
}

export const api = {
  getRoles: () => request("/roles"),
  getRole: (roleId) => request(`/roles/${roleId}`),
  getProjects: (roleId) => request(`/roles/${roleId}/projects`),
  getLearningPath: (roleId) => request(`/roles/${roleId}/learning-path`),
  getSimilarRoles: (roleId) => request(`/roles/${roleId}/similar`),
  getSkillGap: (sourceId, targetId) =>
    request(`/roles/${sourceId}/skill-gap/${targetId}`),
  search: (query) => request(`/search?q=${encodeURIComponent(query)}`),
};
