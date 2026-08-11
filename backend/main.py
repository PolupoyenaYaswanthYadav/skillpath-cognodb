import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.database import db
from backend.services.graph_service import (
    get_learning_path,
    get_role,
    get_role_projects,
    get_roles,
    get_similar_roles,
    get_skill_gap,
    search_graph,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        db.verify_connectivity()
        print("✓ CognoDB connectivity verified")
    except Exception as exc:
        print(f"⚠ Database unavailable: {exc}")

    yield

    db.close()


app = FastAPI(
    title="SkillPath API",
    description="Graph-powered career exploration API backed by CognoDB.",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    try:
        db.verify_connectivity()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        return {
            "status": "degraded",
            "database": "unavailable",
        }


@app.get("/api/roles")
def roles():
    try:
        return get_roles()

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve roles from the graph database.",
        ) from exc


@app.get("/api/roles/{role_id}")
def role_detail(role_id: str):
    try:
        results = get_role(role_id)

        if not results:
            raise HTTPException(
                status_code=404,
                detail="Role not found.",
            )

        return results[0]

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve role information.",
        ) from exc


@app.get("/api/roles/{role_id}/projects")
def role_projects(role_id: str):
    try:
        return get_role_projects(role_id)

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve related projects.",
        ) from exc


@app.get("/api/roles/{role_id}/learning-path")
def learning_path(role_id: str):
    try:
        return get_learning_path(role_id)

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve learning recommendations.",
        ) from exc


@app.get("/api/roles/{role_id}/similar")
def similar_roles(
    role_id: str,
    limit: int = Query(default=5, ge=1, le=20),
):
    try:
        return get_similar_roles(role_id, limit)

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve similar roles.",
        ) from exc


@app.get("/api/roles/{source_role_id}/skill-gap/{target_role_id}")
def skill_gap(
    source_role_id: str,
    target_role_id: str,
):
    try:
        return get_skill_gap(
            source_role_id,
            target_role_id,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to calculate the skill gap.",
        ) from exc


@app.get("/api/search")
def search(
    q: str = Query(min_length=2, max_length=100),
):
    try:
        return search_graph(q)

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Unable to search the graph.",
        ) from exc
