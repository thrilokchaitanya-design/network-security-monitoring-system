import "./NetworkTopology.css";


function NetworkTopology({ hosts }) {
  return (
    <section className="topology-section">
      <div className="section-heading">
        <div>
          <h2>Network Topology</h2>
          <p>Current network structure and connected hosts.</p>
        </div>
      </div>

      <div className="topology-card">
        <div className="topology-node host-node">
          <span className="node-status online"></span>
          <strong>Host 1</strong>
          <span>10.10.10.10</span>
        </div>

        <div className="topology-link"></div>

        <div className="topology-node switch-node">
          <span className="node-icon">◆</span>
          <strong>Switch</strong>
          <span>SW-01</span>
        </div>

        <div className="topology-link"></div>

        <div className="topology-node host-node">
          <span className="node-status online"></span>
          <strong>Host 2</strong>
          <span>192.168.1.100</span>
        </div>
      </div>
    </section>
  );
}

export default NetworkTopology;