import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../services/api";

function AlertDetails() {
  const { id } = useParams();

  const [alert, setAlert] = useState(null);
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");

  const token = localStorage.getItem("access_token");

  const authHeaders = {
    Authorization: `Bearer ${token}`,
  };

  const fetchAlertData = async () => {
    try {
      setError("");

      const [alertResponse, actionsResponse] = await Promise.all([
        api.get(`/alerts/${id}`),
        api.get(`/alerts/${id}/actions`),
      ]);

      setAlert(alertResponse.data);
      setActions(actionsResponse.data);
    } catch (err) {
      console.error("ALERT DETAILS ERROR:", err);
      console.error("RESPONSE:", err.response?.data);

      setError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to load alert details."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlertData();
  }, [id]);

  const performAction = async (action) => {
    try {
      setActionLoading(true);
      setActionError("");

      await api.post(
        `/alerts/${id}/actions`,
        {
          action,
          details: `Action ${action.toLowerCase()} from dashboard`,
        },
        {
          headers: authHeaders,
        }
      );

      await fetchAlertData();
    } catch (err) {
      console.error("ALERT ACTION ERROR:", err);
      console.error("RESPONSE:", err.response?.data);

      setActionError(
        err.response?.data?.detail ||
          err.message ||
          "Failed to perform alert action."
      );
    } finally {
      setActionLoading(false);
    }
  };

  const getSeverityClass = (severity) => {
    if (!severity) return "";

    return severity.toLowerCase();
  };

  const getStatusClass = (status) => {
    if (!status) return "";

    return status.toLowerCase();
  };

  if (loading) {
    return (
      <div className="page-container">
        <p>Loading alert details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <Link to="/dashboard" className="back-link">
          ← Back to Dashboard
        </Link>

        <div className="error-card">
          <h2>Unable to load alert</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!alert) {
    return (
      <div className="page-container">
        <Link to="/dashboard" className="back-link">
          ← Back to Dashboard
        </Link>

        <div className="error-card">
          <h2>Alert not found</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <Link to="/dashboard" className="back-link">
          ← Back to Dashboard
        </Link>

        <div className="alert-title-row">
          <div>
            <p className="eyebrow">SECURITY ALERT</p>

            <h1>Alert Details</h1>

            <p className="page-subtitle">
              Detailed information and activity history for this security
              event.
            </p>
          </div>

          <span
            className={`severity-badge ${getSeverityClass(
              alert.severity
            )}`}
          >
            {alert.severity}
          </span>
        </div>
      </div>

      {actionError && (
        <div className="action-error">
          {actionError}
        </div>
      )}

      <div className="details-grid">
        <section className="details-card">
          <div className="card-header">
            <h2>Threat Information</h2>
          </div>

          <div className="details-list">
            <div className="detail-row">
              <span>Attack Type</span>
              <strong>{alert.attack_type}</strong>
            </div>

            <div className="detail-row">
              <span>Alert ID</span>
              <strong>#{alert.id}</strong>
            </div>

            <div className="detail-row">
              <span>Status</span>

              <strong
                className={`status-badge ${getStatusClass(
                  alert.status
                )}`}
              >
                {alert.status}
              </strong>
            </div>

            <div className="detail-row">
              <span>Confidence</span>
              <strong>
                {alert.confidence_score !== null &&
                alert.confidence_score !== undefined
                  ? `${Number(alert.confidence_score)}%`
                  : "N/A"}
              </strong>
            </div>

            <div className="detail-row">
              <span>Host ID</span>
              <strong>
                {alert.host_id !== null &&
                alert.host_id !== undefined
                  ? alert.host_id
                  : "N/A"}
              </strong>
            </div>

            <div className="detail-row">
              <span>Timestamp</span>
              <strong>
                {new Date(alert.timestamp).toLocaleString()}
              </strong>
            </div>
          </div>
        </section>

        <section className="details-card">
          <div className="card-header">
            <h2>Network Information</h2>
          </div>

          <div className="network-flow">
            <div className="ip-box">
              <span>Source IP</span>
              <strong>{alert.source_ip}</strong>
            </div>

            <div className="flow-arrow">→</div>

            <div className="ip-box">
              <span>Destination IP</span>
              <strong>{alert.destination_ip}</strong>
            </div>
          </div>
        </section>

        <section className="details-card full-width">
          <div className="card-header">
            <h2>Description</h2>
          </div>

          <p className="description">
            {alert.description || "No description provided."}
          </p>
        </section>

        <section className="details-card full-width">
          <div className="card-header">
            <div>
              <h2>Alert Actions</h2>
              <p>Update the current investigation status.</p>
            </div>
          </div>

          <div className="action-buttons">
            <button
              type="button"
              onClick={() => performAction("ACKNOWLEDGED")}
              disabled={actionLoading}
            >
              Acknowledge
            </button>

            <button
              type="button"
              onClick={() => performAction("INVESTIGATING")}
              disabled={actionLoading}
            >
              Investigate
            </button>

            <button
              type="button"
              onClick={() => performAction("MITIGATED")}
              disabled={actionLoading}
            >
              Mitigate
            </button>

            <button
              type="button"
              onClick={() => performAction("RESOLVED")}
              disabled={actionLoading}
            >
              Resolve
            </button>
          </div>

          {actionLoading && (
            <p className="action-loading">
              Updating alert...
            </p>
          )}
        </section>

        <section className="details-card full-width">
          <div className="card-header">
            <div>
              <h2>Action History</h2>
              <p>
                {actions.length}{" "}
                {actions.length === 1 ? "recorded action" : "recorded actions"}
              </p>
            </div>
          </div>

          {actions.length === 0 ? (
            <div className="empty-state">
              No actions have been recorded for this alert.
            </div>
          ) : (
            <div className="action-history">
              {actions.map((action) => (
                <div
                  className="action-item"
                  key={action.id}
                >
                  <div className="action-icon">
                    ✓
                  </div>

                  <div className="action-content">
                    <div className="action-top">
                      <strong>{action.action}</strong>

                      <span>
                        {new Date(
                          action.created_at
                        ).toLocaleString()}
                      </span>
                    </div>

                    <p>
                      <strong>Performed by:</strong>{" "}
                      {action.performed_by}
                    </p>

                    {action.details && (
                      <p>
                        <strong>Details:</strong>{" "}
                        {action.details}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default AlertDetails;
