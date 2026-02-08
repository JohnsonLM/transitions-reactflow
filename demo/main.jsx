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

const MACHINE_LAYOUTS = {
  traffic: { direction: "TB" },
  auth: { direction: "LR" },
  device: { direction: "LR" },
  cicd: { direction: "LR" },
};

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
  const [machineInfo, setMachineInfo] = useState(null);
  const [selectedMachine, setSelectedMachine] = useState("traffic");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    // Fetch all graph data and machine info from the Python backend
    Promise.all([
      fetch("http://localhost:5050/graph-data").then((res) => res.json()),
      fetch("http://localhost:5050/machines").then((res) => res.json()),
    ])
      .then(([graphData, machinesData]) => {
        setAllGraphData(graphData);
        setMachineInfo(machinesData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
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
      MACHINE_LAYOUTS[selectedMachine]?.direction || "TB",
    );
    setNodes(layoutedNodes);
    setEdges(layoutedEdges);
  }, [currentData, selectedMachine, setNodes, setEdges]);

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
      <header className="bg-neutral-700 text-white shadow-md px-8 py-6">
        <h1 className="text-2xl font-semibold">
          transition-reactflow Demo
        </h1>
      </header>

      <div className="flex gap-2 px-5 py-4 bg-white border-b border-gray-200 overflow-x-auto">
        {machineInfo &&
          machineInfo.map((info) => (
            <button
              key={info.id}
              className={`flex-1 min-w-44 px-4 py-3 rounded-lg border transition-all text-left ${
                selectedMachine === info.id
                  ? "bg-indigo-600 border-indigo-600 text-white"
                  : "bg-gray-100 border-gray-300 text-gray-900 hover:bg-gray-200 hover:border-gray-400"
              }`}
              onClick={() => setSelectedMachine(info.id)}
            >
              <div className="font-semibold text-sm mb-2 capitalize">
                {info.id.replace("_", " ")}
              </div>
              <div className="text-xs opacity-70 font-mono">
                {info.type}
              </div>
            </button>
          ))}
      </div>

      <div className="flex justify-center items-center px-5 py-3 bg-white border-b border-gray-200">
        {currentData && machineInfo && (
          <div className="flex gap-4 text-sm text-gray-600">
            <span className="font-medium">
              {currentData.nodes.length} states
            </span>
            <span>•</span>
            <span className="font-medium">
              {currentData.edges.length} transitions
            </span>
            <span>•</span>
            <span className="font-mono text-xs bg-gray-100 px-2 py-1 rounded">
              {machineInfo.find((m) => m.id === selectedMachine)?.type}
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
