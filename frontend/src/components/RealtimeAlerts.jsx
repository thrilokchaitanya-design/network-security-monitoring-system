import { useEffect, useState } from "react";
import api from "../services/api";
import "./RealtimeAlerts.css";

function RealtimeAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState("Connecting...");

  useEffect(() => {
    let active = true;
    let socket;
    let reconnectTimer;
    let reconnectDelay = 1000;
    const mergeAlerts = (current, incoming) => {
      const byId = new Map();
      [...incoming, ...current].forEach((alert) => byId.set(alert.id, alert));
      return [...byId.values()]
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        .slice(0, 10);
    };

    api.get("/alerts/recent?limit=10")
      .then(({ data }) => { if (active) setAlerts((current) => mergeAlerts(current, data)); })
      .catch(() => { if (active) setConnectionStatus("Connecting..."); });

    const connect = () => {
      if (!active) return;
      const baseUrl = api.defaults.baseURL || window.location.origin;
      socket = new WebSocket(`${baseUrl.replace(/^http/, "ws")}/ws/alerts`);
      socket.onopen = () => {
        reconnectDelay = 1000;
        setConnectionStatus("Live");
      };
      socket.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          if (message.type === "alert" && message.data) {
            setAlerts((current) => mergeAlerts(current, [message.data]));
          }
        } catch (parseError) {
          console.error("Failed to parse WebSocket message:", parseError);
        }
      };
      socket.onerror = () => socket.close();
      socket.onclose = () => {
        if (!active) return;
        setConnectionStatus("Reconnecting...");
        reconnectTimer = window.setTimeout(connect, reconnectDelay);
        reconnectDelay = Math.min(reconnectDelay * 2, 15000);
      };
    };
    connect();

    return () => {
      active = false;
      window.clearTimeout(reconnectTimer);
      if (socket && socket.readyState <= WebSocket.OPEN) socket.close();
    };
  }, []);

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
    <div className="realtime-alerts">

      {/* HEADER */}

      <div className="realtime-alerts-header">

        <div>
          <h3>Live Security Events</h3>

          <p>
            Alerts received in real time from the monitoring system.
          </p>
        </div>

        <div className="realtime-status">

          <span
            className={`realtime-status-dot ${
              connectionStatus === "Live"
                ? "connected"
                : "disconnected"
            }`}
          ></span>

          <span>
            {connectionStatus}
          </span>

        </div>

      </div>


      {/* ALERTS */}

      {alerts.length === 0 ? (

        <div className="realtime-empty">
          Waiting for security alerts...
        </div>

      ) : (

        <div className="realtime-alert-list">

          {alerts.map((alert, index) => (

            <div
              className="realtime-alert-card"
              key={`${alert.id}-${index}`}
            >

              <div className="realtime-alert-top">

                <div className="realtime-alert-title">

                  <span
                    className={`realtime-severity realtime-severity-${String(
                      alert.severity || "LOW"
                    ).toLowerCase()}`}
                  >
                    {alert.severity}
                  </span>

                  <strong>
                    {alert.attack_type}
                  </strong>

                </div>

                <span className="realtime-new">
                  LIVE
                </span>

              </div>


              <div className="realtime-network">

                <div>
                  <span>
                    Source IP
                  </span>

                  <strong>
                    {alert.source_ip || "N/A"}
                  </strong>
                </div>

                <span className="realtime-arrow">
                  →
                </span>

                <div>
                  <span>
                    Destination IP
                  </span>

                  <strong>
                    {alert.destination_ip || "N/A"}
                  </strong>
                </div>

              </div>


              <div className="realtime-meta">

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

                  <strong>
                    {alert.status || "Active"}
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

                <p className="realtime-description">
                  {alert.description}
                </p>

              )}

            </div>

          ))}

        </div>

      )}

    </div>
  );
}

export default RealtimeAlerts;
