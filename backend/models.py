from typing import Any

from pydantic import BaseModel


class RoleSummary(BaseModel):
    id: str
    name: str
    category: str
    seniority: str


class RoleDetail(BaseModel):
    role_id: str
    role_name: str
    description: str
    category: str
    seniority: str
    skills: list[dict[str, Any]]
    technologies: list[dict[str, Any]]


class SearchResult(BaseModel):
    id: str
    name: str
    type: str
    category: str | None = None
