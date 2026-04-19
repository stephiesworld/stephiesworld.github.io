// Modal.jsx — track detail modal

function TrackModal({ track, open, onClose }) {
  const [playing, setPlaying] = React.useState(false);
  const [progress, setProgress] = React.useState(0);

  React.useEffect(() => {
    setPlaying(false);
    setProgress(0);
  }, [track?.title]);

  React.useEffect(() => {
    if (!playing) return;
    const id = setInterval(() => {
      setProgress(p => {
        if (p >= 100) { setPlaying(false); return 100; }
        return p + (100 / 30); // 30s preview
      });
    }, 1000);
    return () => clearInterval(id);
  }, [playing]);

  React.useEffect(() => {
    const onKey = e => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  if (!track) return null;

  const previewSec = Math.min(30, Math.round((progress / 100) * 30));
  const mm = String(Math.floor(previewSec / 60)).padStart(2, "0");
  const ss = String(previewSec % 60).padStart(2, "0");

  return (
    <div className={`modal-scrim ${open ? "open" : ""}`} onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <button className="close" onClick={onClose}>close ×</button>
        <div className="eyebrow">no. {track.n} · from the canon</div>
        <h3><em>{track.title}</em></h3>
        <div className="by">by {track.artist}</div>

        <div className="player">
          <button
            className="play-btn"
            onClick={() => setPlaying(p => !p)}
            aria-label={playing ? "pause" : "play"}
          >
            {playing ? "❙❙" : "▶"}
          </button>
          <div className="bar" style={{ "--progress": `${progress}%` }} />
          <span className="time">{mm}:{ss}</span>
          <span className="preview-note">30s preview</span>
        </div>

        <div className="specs">
          <div className="item"><span className="k">year</span><span className="v">{track.year}</span></div>
          <div className="item"><span className="k">duration</span><span className="v">{track.duration}</span></div>
          <div className="item"><span className="k">tag</span><span className="v">{track.tag}</span></div>
        </div>

        <p className="quote">
          A track from Stephie's canon — a room you can step into when the day is too loud.
          Let it play; it does not ask anything of you.
        </p>
      </div>
    </div>
  );
}

Object.assign(window, { TrackModal });
