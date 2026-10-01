import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import "./AlertTimeline.css";

function AlertTimeline() {
  const [events, setEvents] = useState([]);
  const [cursor, setCursor] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const visibleEvents = useMemo(() => events.slice(0, cursor + 1), [events, cursor]);

  useEffect(() => {
    let active = true;
    api.get("/alerts/timeline?limit=1000")
      .then(({ data }) => {
        if (!active) return;
        setEvents(data.items || []);
        setCursor(Math.max((data.items || []).length - 1, 0));
      })
      .catch((err) => { if (active) setError(err.response?.data?.detail || "Could not load the alert timeline."); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!playing) return undefined;
    const timer = window.setInterval(() => {
      if (cursor >= events.length - 1) setPlaying(false);
      else setCursor(cursor + 1);
    }, 900);
    return () => window.clearInterval(timer);
  }, [playing, cursor, events.length]);

  const currentEvent = events[cursor];
  const formatTime = (value) => value ? new Date(value).toLocaleString() : "Unknown time";

  return (
    <main className="timeline-page">
      <div className="timeline-container">
        <Link className="timeline-back" to="/dashboard">← Dashboard</Link>
        <header className="timeline-header">
          <div>
            <p className="timeline-eyebrow">EVENT INVESTIGATION</p>
            <h1>Alert Timeline &amp; Replay</h1>
            <p>Review persisted detection events in timestamp order and replay their sequence.</p>
          </div>
          <span className="timeline-count">{events.length} events loaded</span>
        </header>

        {loading && <div className="timeline-message">Loading alert history…</div>}
        {error && <div className="timeline-message timeline-error" role="alert">{error}</div>}
        {!loading && !error && events.length === 0 && <div className="timeline-message">No alert events are available to replay yet.</div>}

        {!loading && !error && events.length > 0 && (
          <>
            <section className="replay-panel" aria-label="Alert replay controls">
              <div className="replay-current">
                <div>
                  <span>Replay position</span>
                  <strong>{cursor + 1} / {events.length}</strong>
                </div>
                <div>
                  <span>Current event time</span>
                  <strong>{formatTime(currentEvent?.timestamp)}</strong>
                </div>
                <button type="button" onClick={() => { if (cursor >= events.length - 1) setCursor(0); setPlaying((value) => !value); }}>
                  {playing ? "Pause replay" : cursor >= events.length - 1 ? "Replay from start" : "Play replay"}
                </button>
              </div>
              <input
                aria-label="Replay alert events"
                type="range"
                min="0"
                max={Math.max(events.length - 1, 0)}
                value={cursor}
                onChange={(event) => { setPlaying(false); setCursor(Number(event.target.value)); }}
              />
              <div className="replay-range"><span>{formatTime(events[0]?.timestamp)}</span><span>{formatTime(events.at(-1)?.timestamp)}</span></div>
            </section>

            <section className="timeline-list" aria-label="Alert event timeline">
              <h2>Event sequence <span>{visibleEvents.length} shown</span></h2>
              {visibleEvents.map((event, index) => (
                <article className={`timeline-event ${index === cursor ? "current" : ""}`} key={event.id}>
                  <div className="timeline-marker" />
                  <div className="timeline-event-body">
                    <div className="timeline-event-top">
                      <span className={`timeline-severity severity-${String(event.severity).toLowerCase()}`}>{event.severity}</span>
                      <time dateTime={event.timestamp}>{formatTime(event.timestamp)}</time>
                    </div>
                    <Link to={`/alerts/${event.id}`} className="timeline-event-title">{event.attack_type} <span>Alert #{event.id}</span></Link>
                    <p>{event.source_ip} <span>→</span> {event.destination_ip}</p>
                    {event.description && <small>{event.description}</small>}
                  </div>
                </article>
              ))}
            </section>
          </>
        )}
      </div>
    </main>
  );
}

export default AlertTimeline;
