import { useEffect, useState } from "react";
import api from "../services/api";
import "./NetworkTopology.css";

function NetworkTopology({ refreshKey = 0, onSourceChange }) {
  const [topology, setTopology] = useState({ nodes: [], links: [], source: "" });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    api.get("/topology")
      .then(({ data }) => {
        if (active) {
          setTopology(data);
          onSourceChange?.(data.source);
        }
      })
      .catch((err) => {
        if (active) setError(err.response?.data?.detail || "Topology data is unavailable.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, [refreshKey, onSourceChange]);

  const switches = topology.nodes.filter((node) => node.type === "switch");
  const hosts = topology.nodes.filter((node) => node.type === "host");
  const sourceLabel = topology.source === "sdn_controller"
    ? "Live SDN controller"
    : "Registered hosts (controller not configured)";

  return (
    <section className="topology-section">
      <div className="section-heading topology-heading">
        <div>
          <h2>Network Topology</h2>
          <p>Topology data from the connected network source.</p>
        </div>
        {!loading && !error && <span className={`topology-source ${topology.source === "sdn_controller" ? "live" : "fallback"}`}>{sourceLabel}</span>}
      </div>

      {loading ? <div className="topology-state">Loading topology…</div> : null}
      {error ? <div className="topology-state topology-error" role="alert">{error}</div> : null}
      {!loading && !error && (
        <div className="topology-card">
          {topology.nodes.length === 0 ? (
            <div className="topology-state">No switches or hosts were reported by the topology source.</div>
          ) : (
            <>
              <div className="topology-group">
                <h3>Switches <span>{switches.length}</span></h3>
                <div className="topology-node-list">
                  {switches.map((node) => (
                    <article className="topology-node switch-node" key={node.id}>
                      <span className="node-status online" />
                      <strong>{node.name || node.dpid || node.id}</strong>
                      {node.dpid && <span>{node.dpid}</span>}
                    </article>
                  ))}
                  {switches.length === 0 && <p className="topology-empty">No switches reported.</p>}
                </div>
              </div>

              <div className="topology-links">
                <h3>Connections <span>{topology.links.length}</span></h3>
                {topology.links.length ? topology.links.map((link, index) => (
                  <div className="topology-connection" key={`${link.source}-${link.target}-${index}`}>
                    <span>{link.source}</span><span className="topology-link-line" aria-label="connected to" /> <span>{link.target}</span>
                  </div>
                )) : <p className="topology-empty">No links reported.</p>}
              </div>

              <div className="topology-group">
                <h3>Hosts <span>{hosts.length}</span></h3>
                <div className="topology-node-list">
                  {hosts.map((node) => (
                    <article className="topology-node host-node" key={node.id}>
                      <span className={`node-status ${node.status === "online" ? "online" : "offline"}`} />
                      <strong>{node.hostname || node.name || node.id}</strong>
                      <span>{node.ip_address || node.mac_address || "Address unavailable"}</span>
                    </article>
                  ))}
                  {hosts.length === 0 && <p className="topology-empty">No hosts reported.</p>}
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </section>
  );
}

export default NetworkTopology;
