# SkillPath — Graph-Powered Career Exploration

SkillPath is a graph-powered web application for exploring relationships between technical career roles, skills, technologies, projects, courses, and companies.

Instead of presenting career information as disconnected lists, SkillPath models these entities as a connected graph. Users can search for a role and explore the skills, technologies, projects, courses, companies, and related roles connected to it.

The application uses **CognoDB** as its graph database and communicates with it through the Neo4j-compatible driver and openCypher.

---

## Overview

When exploring a technical career, a list of required skills is often not enough. A useful career exploration system should help answer connected questions such as:

- What skills does a role require?
- Which technologies are associated with the role?
- What projects demonstrate those skills?
- Which courses teach the required skills?
- Which companies hire for the role?
- Which other roles are similar?
- How are skills connected through prerequisites?

SkillPath represents these relationships directly in a graph and exposes them through a web application.

---

## Why a Graph Database?

Career information is highly relationship-oriented.

A relational database can represent the same entities, but many of the application's useful questions involve traversing several relationships.

For example, SkillPath can traverse:

```text
Role
  │
  ├── REQUIRES ──> Skill
  │                  │
  │                  └── DEMONSTRATED_BY ──> Project
  │
  └── USES ──────> Technology
                     │
                     └── USED_IN ──────────> Project
```

It can also explore prerequisite relationships:

```text
Skill
  │
  └── PREREQUISITE_OF ──> Skill
```

and related career paths:

```text
Role ── SIMILAR_TO ──> Role
```

These multi-hop relationships are central to the application's purpose. The graph model allows the application to traverse connected entities directly instead of repeatedly joining separate relationship tables.

A relational database would still be appropriate for many simpler tabular operations. The graph database is useful here because relationship traversal is a core part of the user experience.

---

## Graph Data Model

The current graph contains:

- **154 nodes**
- **425 relationships**
- **6 node labels**
- **9 relationship types**

### Node Types

| Node | Description |
|---|---|
| `Role` | Technical career roles |
| `Skill` | Skills associated with technical roles |
| `Technology` | Programming languages, frameworks, tools, and platforms |
| `Project` | Practical projects demonstrating skills |
| `Company` | Companies associated with hiring for roles |
| `Course` | Learning resources associated with skills and technologies |

### Relationship Types

| Relationship | Direction | Meaning |
|---|---|---|
| `HIRES_FOR` | Company → Role | Company hires for a role |
| `REQUIRES` | Role → Skill | Role requires a skill |
| `USES` | Role → Technology | Role uses a technology |
| `DEMONSTRATED_BY` | Skill → Project | Project demonstrates a skill |
| `USED_IN` | Technology → Project | Project uses a technology |
| `TEACHES` | Course → Skill | Course teaches a skill |
| `COVERS` | Course → Technology | Course covers a technology |
| `PREREQUISITE_OF` | Skill → Skill | One skill is a prerequisite for another |
| `SIMILAR_TO` | Role → Role | Two roles are considered similar |

### Graph Structure

```text
                         ┌─────────────┐
                         │   Company   │
                         └──────┬──────┘
                                │
                            HIRES_FOR
                                │
                                ▼
                         ┌─────────────┐
                         │    Role     │
                         └──────┬──────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
               REQUIRES                     USES
                  │                           │
                  ▼                           ▼
            ┌──────────┐               ┌────────────┐
            │  Skill   │               │ Technology │
            └────┬─────┘               └─────┬──────┘
                 │                           │
        DEMONSTRATED_BY                    USED_IN
                 │                           │
                 ▼                           ▼
            ┌──────────┐               ┌───────────┐
            │ Project  │               │  Project  │
            └──────────┘               └───────────┘

            ┌──────────┐
            │  Course  │
            └────┬─────┘
                 │
          ┌──────┴──────┐
          │             │
       TEACHES        COVERS
          │             │
          ▼             ▼
        Skill       Technology

        Skill ── PREREQUISITE_OF ──> Skill

        Role ───── SIMILAR_TO ─────> Role
```

---

## Seed Data

The repository contains seed data in JSON format:

```text
data/
├── companies.json
├── courses.json
├── projects.json
├── roles.json
├── skills.json
└── technologies.json
```

The seed data is transformed into the graph using the included Python seed script.

The current seeded graph contains 154 nodes and 425 relationships.

---

## Architecture

```text
┌──────────────────────────────┐
│          React UI            │
│                              │
│  Search                      │
│  Role Explorer               │
│  Role Details                │
│  Graph Visualization         │
│  Projects / Courses          │
└──────────────┬───────────────┘
               │ HTTP / JSON
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│                              │
│  API endpoints               │
│  Request handling            │
│  Error handling              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Neo4j Python Driver      │
│                              │
│     Parameterized Cypher     │
└──────────────┬───────────────┘
               │ Bolt
               ▼
┌──────────────────────────────┐
│          CognoDB             │
│                              │
│  Nodes                       │
│  Relationships               │
│  Constraints                 │
└──────────────────────────────┘
```

---

## Graph Queries

The Cypher queries are stored under:

```text
database/queries/
```

### Role Overview

`role_overview.cypher`

Retrieves information connected to a selected role, including its required skills and associated technologies.

### Role Projects

`role_projects.cypher`

Uses the multi-hop traversal:

```text
Role
  ↓ REQUIRES
Skill
  ↓ DEMONSTRATED_BY
Project
```

This allows the application to find projects relevant to the skills required by a role.

### Learning Path

`learning_path.cypher`

Connects role requirements with relevant learning resources through the skill relationships.

### Similar Roles

`similar_roles.cypher`

Uses the `SIMILAR_TO` relationship to discover related career paths.

### Skill Gap

`skill_gap.cypher`

Compares skill requirements between roles to identify differences between career paths.

---

## Parameterized Cypher

The backend uses parameterized Cypher queries through the Neo4j Python driver.

Example:

```cypher
MATCH (r:Role {id: $role_id})-[:REQUIRES]->(s:Skill)
RETURN r, s
```

The `role_id` value is supplied separately rather than being directly concatenated into the query.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Neo4j Python Driver
- openCypher

### Database

- CognoDB Cloud
- Bolt protocol
- Neo4j-compatible graph model

### Frontend

- React
- Vite
- React Flow
- Lucide React

---

## Project Structure

```text
skillpath-cognodb/
│
├── backend/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── services/
│       └── graph_service.py
│
├── data/
│   ├── companies.json
│   ├── courses.json
│   ├── projects.json
│   ├── roles.json
│   ├── skills.json
│   └── technologies.json
│
├── database/
│   ├── queries/
│   │   ├── learning_path.cypher
│   │   ├── role_overview.cypher
│   │   ├── role_projects.cypher
│   │   ├── similar_roles.cypher
│   │   └── skill_gap.cypher
│   │
│   └── schema/
│       └── constraints.cypher
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       ├── App.css
│       ├── App.jsx
│       ├── index.css
│       └── main.jsx
│
├── scripts/
│   ├── apply_schema.py
│   ├── seed.py
│   ├── test_connection.py
│   ├── test_queries.py
│   ├── verify_graph.py
│   └── verify_schema.py
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Environment Variables

Database credentials are stored locally in `.env`.

Example:

```env
COGNODB_URI=bolt+s://<instance-id>.databases.cognodb.cloud
COGNODB_USERNAME=cognodb
COGNODB_PASSWORD=<your-password>
```

`.env` is excluded from Git through `.gitignore`.

**Never commit the actual database password or other credentials.**

---

## Verification

The repository includes scripts for verifying the database and graph:

```bash
python scripts/test_connection.py
python scripts/test_queries.py
python scripts/verify_schema.py
python scripts/verify_graph.py
```

The current graph verification reports:

```text
=== NODE COUNTS ===

Role          15
Skill         44
Technology    30
Project       25
Company       20
Course        20

=== TOTALS ===

Nodes:        154
Relationships: 425
```

---

## UI Features

The application currently provides:

- Career role search
- Role exploration
- Role detail pages
- Interactive graph visualization
- Skill information
- Technology information
- Project recommendations
- Course recommendations
- Similar role exploration
- Loading states
- Connection error states

---

## Screenshots

Screenshots of the completed application will be added here before final submission.

---

## Local Development

### Backend

Create and activate the Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies and configure the `.env` file.

Then start FastAPI:

```bash
uvicorn backend.main:app --reload
```

The backend runs on:

```text
http://127.0.0.1:8000
```

### Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

The frontend runs on:

```text
http://localhost:5173
```

Both the backend and frontend must be running for the complete application to work locally.

---

## Design Decisions

### Graph-first data model

Roles, skills, technologies, projects, courses, and companies are modeled as connected entities rather than isolated records.

### Separate Cypher files

Cypher queries are stored separately from the API code to keep graph logic easier to inspect and maintain.

### Parameterized queries

Query parameters are used instead of constructing Cypher strings through direct value concatenation.

### Interactive visualization

The application uses an interactive graph so users can visually understand the connections between career entities.

### JSON seed data

JSON provides a simple and transparent source format for recreating the graph dataset.

---

## Future Improvements

Potential extensions include:

- More detailed skill-gap visualization
- Personalized career recommendations
- Richer prerequisite learning paths
- Role transition analysis
- Additional graph analytics
- Larger real-world datasets

These are outside the scope of the current implementation.

---

## License

This project was created as a technical take-home assignment for Wexa AI.