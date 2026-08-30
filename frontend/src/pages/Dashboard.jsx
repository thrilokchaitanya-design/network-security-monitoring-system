import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import NetworkTopology from "../components/NetworkTopology";
import RealtimeAlerts from "../components/RealtimeAlerts";
import "./Dashboard.css";

function Dashboard() {
  const [alerts, setAlerts] = useState([]);
  const [hosts, setHosts] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [attackDistribution, setAttackDistribution] = useState([]);
  const [severityDistribution, setSeverityDistribution] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSecurityData = async () => {
      try {
        const token = localStorage.getItem("access_token");

        if (!token) {
          throw new Error("No access token found");
        }

        const headers = {
          Authorization: `Bearer ${token}`,
        };

        const [
          alertsResponse,
          hostsResponse,
          analyticsResponse,
          attacksResponse,
          severityResponse,
        ] = await Promise.all([
          api.get("/alerts", { headers }),
          api.get("/hosts", { headers }),
          api.get("/analytics/summary", { headers }),
          api.get("/analytics/attacks", { headers }),
          api.get("/analytics/severity", { headers }),
        ]);

        setAlerts(alertsResponse.data.items || []);
        setHosts(hostsResponse.data || []);
        setAnalytics(analyticsResponse.data);
        setAttackDistribution(attacksResponse.data || []);
        setSeverityDistribution(severityResponse.data || []);
      } catch (err) {
        console.error("SECURITY DATA ERROR:", err);

        setError(
          err.response?.data?.detail ||
            err.message ||
            "Failed to load security data."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchSecurityData();
  }, []);

  const criticalAlerts =
    analytics?.severity?.critical ?? 0;

  const formatConfidence = (confidence) => {
    if (confidence === null || confidence === undefined) {
      return "N/A";
    }

    const numericConfidence = Number(confidence);

    if (Number.isNaN(numericConfidence)) {
      return "N/A";
    }

    const percentage =
      numericConfidence <= 1
        ? numericConfidence * 100
        : numericConfidence;

    return `${Number(percentage.toFixed(2))}%`;
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">

        {/* =====================================================
            HEADER
            ===================================================== */}

        <header className="dashboard-header">
          <div>
            <p className="dashboard-eyebrow">
              NETWORK SECURITY
            </p>

            <h1>Capstone Security Dashboard</h1>

            <p className="dashboard-subtitle">
              Welcome to the Network Security Monitoring System.
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={() => window.location.reload()}
          >
            Refresh Data
          </button>
        </header>


        {/* =====================================================
            LOADING
            ===================================================== */}

        {loading && (
          <div className="dashboard-message">
            Loading security data...
          </div>
        )}


        {/* =====================================================
            ERROR
            ===================================================== */}

        {error && (
          <div className="dashboard-error">
            Failed to load security data: {error}
          </div>
        )}


        {!loading && !error && (
          <>


            {/* =================================================
                1. SYSTEM STATUS
                ================================================= */}

            <section className="dashboard-section">

              <div className="section-heading">
                <h2>System Status</h2>
              </div>

              <div className="status-grid">

                <div className="status-card">

                  <span className="status-dot online"></span>

                  <div>
                    <span className="status-label">
                      Backend
                    </span>

                    <strong>
                      Connected
                    </strong>
                  </div>

                </div>


                <div className="status-card">

                  <span className="status-dot pending"></span>

                  <div>
                    <span className="status-label">
                      AI Detection
                    </span>

                    <strong>
                      Pending
                    </strong>
                  </div>

                </div>


                <div className="status-card">

                  <span className="status-dot pending"></span>

                  <div>
                    <span className="status-label">
                      SDN Controller
                    </span>

                    <strong>
                      Pending
                    </strong>
                  </div>

                </div>

              </div>

            </section>


            {/* =================================================
                2. SECURITY OVERVIEW
                ================================================= */}

            <section className="dashboard-section">

              <div className="section-heading">
                <h2>Security Overview</h2>
              </div>

              <div className="overview-grid">

                <div className="overview-card">

                  <span className="overview-label">
                    Total Alerts
                  </span>

                  <strong>
                    {analytics?.total_alerts ?? 0}
                  </strong>

                </div>


                <div className="overview-card">

                  <span className="overview-label">
                    Active Alerts
                  </span>

                  <strong>
                    {analytics?.active_alerts ?? 0}
                  </strong>

                </div>


                <div className="overview-card">

                  <span className="overview-label">
                    Critical Alerts
                  </span>

                  <strong>
                    {criticalAlerts}
                  </strong>

                </div>


                <div className="overview-card">

                  <span className="overview-label">
                    Resolved Alerts
                  </span>

                  <strong>
                    {analytics?.resolved_alerts ?? 0}
                  </strong>

                </div>


                <div className="overview-card">

                  <span className="overview-label">
                    Average Confidence
                  </span>

                  <strong>
                    {formatConfidence(
                      analytics?.average_confidence
                    )}
                  </strong>

                </div>


                <div className="overview-card">

                  <span className="overview-label">
                    Active Hosts
                  </span>

                  <strong>
                    {hosts.length}
                  </strong>

                </div>

              </div>

            </section>


            {/* =================================================
                3. REAL-TIME ALERTS
                ================================================= */}

            <section className="dashboard-section">

              <div className="section-heading">

                <div>
                  <h2>
                    Real-Time Alerts
                  </h2>

                  <p>
                    Live security events received from the monitoring system.
                  </p>
                </div>

              </div>

              <RealtimeAlerts />

            </section>


            {/* =================================================
                4. SECURITY DISTRIBUTION
                ================================================= */}

            <section className="dashboard-section">

              <div className="section-heading">

                <div>
                  <h2>
                    Security Distribution
                  </h2>

                  <p>
                    Current alert severity and attack-type distribution.
                  </p>
                </div>

              </div>


              <div className="analytics-grid">


                {/* SEVERITY */}

                <div className="analytics-card">

                  <h3>
                    Severity
                  </h3>

                  {severityDistribution.length === 0 ? (

                    <p>
                      No severity data available.
                    </p>

                  ) : (

                    <div className="distribution-list">

                      {severityDistribution.map((item) => (

                        <div
                          className="distribution-row"
                          key={item.severity}
                        >

                          <span>
                            {item.severity}
                          </span>

                          <strong>
                            {item.count}
                          </strong>

                        </div>

                      ))}

                    </div>

                  )}

                </div>


                {/* ATTACK TYPES */}

                <div className="analytics-card">

                  <h3>
                    Attack Types
                  </h3>

                  {attackDistribution.length === 0 ? (

                    <p>
                      No attack data available.
                    </p>

                  ) : (

                    <div className="distribution-list">

                      {attackDistribution.map((item) => (

                        <div
                          className="distribution-row"
                          key={item.attack_type}
                        >

                          <span>
                            {item.attack_type}
                          </span>

                          <strong>
                            {item.count}
                          </strong>

                        </div>

                      ))}

                    </div>

                  )}

                </div>

              </div>

            </section>


            {/* =================================================
                5. NETWORK TOPOLOGY
                ================================================= */}

            <section className="dashboard-section">

              <NetworkTopology />

            </section>


            {/* =================================================
                6. RECENT ALERTS
                ================================================= */}

            <section className="dashboard-section">

              <div className="section-heading">

                <div>
                  <h2>
                    Recent Alerts
                  </h2>

                  <p>
                    Security events detected by the monitoring system.
                  </p>
                </div>

              </div>


              <div className="alerts-list">

                {alerts.length === 0 ? (

                  <div className="empty-state">

                    <p>
                      No alerts found.
                    </p>

                  </div>

                ) : (

                  alerts.map((alert) => (

                    <Link
                      to={`/alerts/${alert.id}`}
                      key={alert.id}
                      className="alert-card"
                    >

                      <div className="alert-card-top">

                        <div className="alert-title">

                          <span
                            className={`severity-badge severity-${alert.severity.toLowerCase()}`}
                          >
                            {alert.severity}
                          </span>

                          <span className="alert-attack">
                            {alert.attack_type}
                          </span>

                        </div>

                        <span className="alert-arrow">
                          View Details →
                        </span>

                      </div>


                      <div className="alert-network">

                        <div>

                          <span className="network-label">
                            Source IP
                          </span>

                          <strong>
                            {alert.source_ip}
                          </strong>

                        </div>


                        <span className="network-arrow">
                          →
                        </span>


                        <div>

                          <span className="network-label">
                            Destination IP
                          </span>

                          <strong>
                            {alert.destination_ip}
                          </strong>

                        </div>

                      </div>


                      <div className="alert-meta">

                        <div>

                          <span>
                            Confidence
                          </span>

                          <strong>
                            {formatConfidence(
                              alert.confidence_score
                            )}
                          </strong>

                        </div>


                        <div>

                          <span>
                            Status
                          </span>

                          <strong className="alert-status">
                            {alert.status}
                          </strong>

                        </div>


                        <div>

                          <span>
                            Alert ID
                          </span>

                          <strong>
                            #{alert.id}
                          </strong>

                        </div>

                      </div>


                      {alert.description && (

                        <p className="alert-description">
                          {alert.description}
                        </p>

                      )}

                    </Link>

                  ))

                )}

              </div>

            </section>

          </>
        )}

      </div>
    </div>
  );
}

export default Dashboard;