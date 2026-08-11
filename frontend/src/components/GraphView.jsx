import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

function createNodes(role, skills, technologies) {
  const nodes = [
    {
      id: "role",
      position: { x: 350, y: 230 },
      data: { label: role.role_name },
      style: {
        background: "#111827",
        color: "white",
        border: "none",
        borderRadius: 14,
        padding: "14px 20px",
        fontWeight: 700,
        minWidth: 170,
        textAlign: "center",
      },
    },
  ];

  skills.slice(0, 7).forEach((skill, index) => {
    nodes.push({
      id: `skill-${skill.id}`,
      position: {
        x: 40 + (index % 4) * 180,
        y: index < 4 ? 30 : 430,
      },
      data: { label: skill.name },
      style: {
        background: "#f8fafc",
        color: "#334155",
        border: "1px solid #cbd5e1",
        borderRadius: 12,
        padding: "10px 14px",
      },
    });
  });

  technologies.slice(0, 5).forEach((technology, index) => {
    nodes.push({
      id: `tech-${technology.id}`,
      position: {
        x: 100 + index * 190,
        y: 650,
      },
      data: { label: technology.name },
      style: {
        background: "#eef2ff",
        color: "#3730a3",
        border: "1px solid #c7d2fe",
        borderRadius: 12,
        padding: "10px 14px",
      },
    });
  });

  return nodes;
}

function createEdges(skills, technologies) {
  const edges = skills.slice(0, 7).map((skill) => ({
    id: `role-${skill.id}`,
    source: "role",
    target: `skill-${skill.id}`,
    animated: true,
  }));

  technologies.slice(0, 5).forEach((technology) => {
    edges.push({
      id: `tech-${technology.id}`,
      source: "role",
      target: `tech-${technology.id}`,
    });
  });

  return edges;
}

export default function GraphView({ role, skills, technologies }) {
  const nodes = createNodes(role, skills, technologies);
  const edges = createEdges(skills, technologies);

  return (
    <div className="graph-container">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        nodesDraggable
        nodesConnectable={false}
        proOptions={{ hideAttribution: true }}
      >
        <Background gap={24} size={1} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
