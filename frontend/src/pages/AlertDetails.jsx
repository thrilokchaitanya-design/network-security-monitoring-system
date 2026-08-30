import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import "./AlertDetails.css";

function AlertDetails() {
  const { alertId } = useParams();
  const navigate = useNavigate();

  const [alert, setAlert] = useState(null);
  const [actions, setActions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");

  const fetchAlertDetails = async () => {
    try {
      setError("");

      const token = localStorage.getItem("access_token");

      if (!token) {
        navigate("/");
        return;
      }

      const headers = {
        Authorization: `Bearer ${token}`,
      };

      const [alertResponse, actionsResponse] = await Promise.all([
        api.get(`/alerts/${alertId}`, { headers }),
        api.get(`/alerts/${alertId}/actions`, { headers }),
      ]);

      setAlert(alertResponse.data);

      setActions(
        Array.isArray(actionsResponse.data)
          ? actionsResponse.data
          : actionsResponse.data.items || []
      );
    } catch (err) {
      console.error("ALERT DETAILS ERROR:", err);
      console.error("RESPONSE:", err.response?.data);

      if (err.response?.status === 401) {
        localStorage.removeItem("access_token");
        navigate("/");
        return;
      }

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
    fetchAlertDetails();
  }, [alertId]);

  const performAction = async (action) => {
    try {
      setActionLoading(true);
      setActionError("");

      const token = localStorage.getItem("access_token");

      if (!token) {
        navigate("/");
        return;
      }

      await api.post(
        `/alerts/${alertId}/actions`,
        {
          action: action,
          details: `Action ${action.toLowerCase()} from dashboard`,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      await fetchAlertDetails();
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

  const formatConfidence = (value) => {
    if (value === null || value === undefined) {
      return "N/A";
    }

    const number = Number(value);

    if (Number.isNaN(number)) {
      return "N/A";
    }

    return `${number}%`;
  };

  const formatTimestamp = (value) => {
    if (!value) {
      return "N/A";
    }

    return new Date(value).toLocaleString();
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-state">
          <p>Loading alert details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="page-container">
        <button
          className="back-button"
          onClick={() => navigate("/dashboard")}
        >
          ← Back to Dashboard
        </button>

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
        <button
          className="back-button"
          onClick={() => navigate("/dashboard")}
        >
          ← Back to Dashboard
        </button>

        <div className="error-card">
          <h2>Alert not found</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <button
        className="back-button"
        onClick={() => navigate("/dashboard")}
      >
        ← Back to Dashboard
      </button>

      <div className="alert-details-header">
        <div>
          <p className="eyebrow">SECURITY ALERT</p>

          <h1>Alert Details</h1>

          <p className="page-subtitle">
            Detailed information and activity history for this security event.
          </p>
        </div>

        <div className="severity-badge">
          {alert.severity}
        </div>
      </div>

      {actionError && (
        <div className="action-error">
          {actionError}
        </div>
      )}

      <div className="details-grid">
        {/* THREAT INFORMATION */}

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
              <strong className="status-badge">
                {alert.status}
              </strong>
            </div>

            <div className="detail-row">
              <span>Confidence</span>
              <strong>
                {formatConfidence(alert.confidence_score)}
              </strong>
            </div>

            <div className="detail-row">
              <span>Host ID</span>
              <strong>
                {alert.host_id ?? "N/A"}
              </strong>
            </div>

            <div className="detail-row">
              <span>Timestamp</span>
              <strong>
                {formatTimestamp(alert.timestamp)}
              </strong>
            </div>
          </div>
        </section>

        {/* NETWORK INFORMATION */}

        <section className="details-card">
          <div className="card-header">
            <h2>Network Information</h2>
          </div>

          <div className="network-flow">
            <div className="ip-box">
              <span>Source IP</span>
              <strong>{alert.source_ip}</strong>
            </div>

            <div className="flow-arrow">
              ↓
            </div>

            <div className="ip-box">
              <span>Destination IP</span>
              <strong>{alert.destination_ip}</strong>
            </div>
          </div>
        </section>

        {/* DESCRIPTION */}

        <section className="details-card full-width">
          <div className="card-header">
            <h2>Description</h2>
          </div>

          <p className="description">
            {alert.description || "No description provided."}
          </p>
        </section>

        {/* ALERT ACTIONS */}

        <section className="details-card full-width">
          <div className="card-header">
            <div>
              <h2>Alert Actions</h2>

              <p>
                Update the current investigation status.
              </p>
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

        {/* ACTION HISTORY */}

        <section className="details-card full-width">
          <div className="card-header">
            <div>
              <h2>Action History</h2>

              <p>
                {actions.length}{" "}
                {actions.length === 1
                  ? "recorded action"
                  : "recorded actions"}
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
                      <strong>
                        {action.action}
                      </strong>

                      <span>
                        {formatTimestamp(
                          action.created_at
                        )}
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