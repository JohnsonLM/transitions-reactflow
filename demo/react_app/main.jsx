import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom/client";
import dagre from "dagre";
import ReactFlow, {
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from "reactflow";
import "reactflow/dist/style.css";

const MACHINES = [
  {
    id: "order",
    name: "E-commerce Order",
    description: "Order processing with validations and error handling",
    direction: "TB",
  },
  {
    id: "auth",
    name: "Authentication",
    description: "User login flow with MFA and lockout",
    direction: "LR",
  },
  {
    id: "document",
    name: "Document Workflow",
    description: "Draft, review, publish cycle",
    direction: "TB",
  },
  {
    id: "traffic",
    name: "Traffic Light",
    description: "Simple 3-state cycle",
    direction: "TB",
  },
  {
    id: "cicd",
    name: "CI/CD Pipeline",
    description: "Build, test, and deploy flow",
    direction: "LR",
  },
];

const getLayoutedElements = (nodes, edges, direction = "TB") => {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: direction, nodesep: 80, ranksep: 120 });

  nodes.forEach((node) => {
    g.setNode(node.id, { width: 150, height: 60 });
  });

  edges.forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const layoutedNodes = nodes.map((node) => {
    const pos = g.node(node.id);
    return {
      ...node,
      position: { x: pos.x - 75, y: pos.y - 30 },
      sourcePosition: direction === "TB" ? "bottom" : "right",
      targetPosition: direction === "TB" ? "top" : "left",
    };
  });

  return [layoutedNodes, edges];
};

export default function App() {
  const [allGraphData, setAllGraphData] = useState(null);
  const [selectedMachine, setSelectedMachine] = useState("order");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    // Fetch all graph data from the Python backend
    fetch("http://localhost:5050/graph-data")
      .then((res) => res.json())
      .then((data) => {
        setAllGraphData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching graph data:", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const currentData = allGraphData?.[selectedMachine];

  useEffect(() => {
    if (!currentData) return;

    const flowNodes = currentData.nodes.map((node) => ({
      id: node.id,
      data: { label: node.data?.label || node.id },
      position: { x: 0, y: 0 },
      className:
        "rounded px-4 py-3 min-w-max text-center font-medium border-2 border-gray-800 text-sm bg-white",
    }));

    const flowEdges = currentData.edges.map((edge) => ({
      id: edge.id || `${edge.source}-${edge.target}`,
      source: edge.source,
      target: edge.target,
      label: edge.label || "",
      type: "smooth",
    }));

    const [layoutedNodes, layoutedEdges] = getLayoutedElements(
      flowNodes,
      flowEdges,
      MACHINES.find((m) => m.id === selectedMachine)?.direction || "TB"
    );
    setNodes(layoutedNodes);
    setEdges(layoutedEdges);
  }, [currentData, setNodes, setEdges]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen text-lg font-medium text-indigo-600 bg-blue-50">
        Loading state machines...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen text-lg font-medium text-red-600 bg-red-50">
        Error loading graphs: {error}
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-gradient-to-r from-indigo-600 to-indigo-800 text-white shadow-md px-8 py-6">
        <h1 className="text-3xl font-semibold mb-1">
          State Machine Visualizer
        </h1>
        <p className="text-sm opacity-90">transitions_rf - React Flow Demo</p>
      </header>

      <div className="flex gap-2 px-5 py-4 bg-white border-b border-gray-200 overflow-x-auto">
        {MACHINES.map((machine) => (
          <button
            key={machine.id}
            className={`flex-1 min-w-40 px-4 py-3 rounded-lg border transition-all text-left ${
              selectedMachine === machine.id
                ? "bg-indigo-600 border-indigo-600 text-white"
                : "bg-gray-100 border-gray-300 text-gray-900 hover:bg-gray-200 hover:border-gray-400"
            }`}
            onClick={() => setSelectedMachine(machine.id)}
          >
            <div className="font-semibold text-sm mb-1">{machine.name}</div>
            <div className="text-xs opacity-80 leading-tight">
              {machine.description}
            </div>
          </button>
        ))}
      </div>

      <div className="flex justify-center items-center px-5 py-3 bg-white border-b border-gray-200">
        {currentData && (
          <div className="flex gap-3 text-sm text-gray-600">
            <span className="font-medium">
              {currentData.nodes.length} states
            </span>
            <span>•</span>
            <span className="font-medium">
              {currentData.edges.length} transitions
            </span>
          </div>
        )}
      </div>

      {currentData && (
        <div className="flex-1 bg-gray-50">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            fitView
          >
            <Background />
            <Controls />
          </ReactFlow>
        </div>
      )}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
