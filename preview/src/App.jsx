// App.jsx — the music page

const DEFAULTS = /*EDITMODE-BEGIN*/{
  "palette": "cream",
  "density": "3",
  "motion": "on",
  "grain": 0.06
}/*EDITMODE-END*/;

function App() {
  const [tweaks, setTweaks] = React.useState(DEFAULTS);
  const [editVisible, setEditVisible] = React.useState(false);
  const [modalTrack, setModalTrack] = React.useState(null);
  const [previewingId, setPreviewingId] = React.useState(null);
  const [selectedMix, setSelectedMix] = React.useState(null);

  // apply tweaks to body
  React.useEffect(() => {
    document.body.dataset.palette = tweaks.palette;
    document.body.dataset.density = tweaks.density;
    document.body.dataset.motion = tweaks.motion;
    document.body.style.setProperty("--grain-intensity", String(tweaks.grain));
  }, [tweaks]);

  // edit mode bridge
  React.useEffect(() => {
    const onMsg = (e) => {
      if (!e?.data || typeof e.data !== "object") return;
      if (e.data.type === "__activate_edit_mode") setEditVisible(true);
      if (e.data.type === "__deactivate_edit_mode") setEditVisible(false);
    };
    window.addEventListener("message", onMsg);
    try { window.parent.postMessage({ type: "__edit_mode_available" }, "*"); } catch (e) {}
    return () => window.removeEventListener("message", onMsg);
  }, []);

  const now = window.NOW_OBSESSED;
  const mixtapes = window.MIXTAPES;
  const favorites = window.FAVORITES;

  return (
    <>
      <div className="page">

        {/* top nav */}
        <nav className="topnav">
          <a className="back" href="World_A.html"><span className="arrow">←</span><em>back to stephie's world</em></a>
          <div className="crumbs"><em>an archive</em> / <em>music</em></div>
        </nav>

        {/* hero */}
        <header className="hero" data-screen-label="01 Hero">
          <div className="hero-constellation"><HeroConstellation /></div>
          <div className="eyebrow label">vol. ii · an archive of sound</div>
          <h1>Music<span className="amp">.</span></h1>
          <p className="lede">
            A quiet catalogue of the songs and mixtapes I keep returning to —
            kept here the way one might keep letters, or small found stones.
          </p>
          <div className="rule" />
        </header>

        {/* now obsessed */}
        <section className="section" data-screen-label="02 Now Obsessed">
          <div className="section-head">
            <h2 className="heading"><span className="num">i.</span><em>Now, on repeat</em></h2>
            <div className="meta">
              <div>currently · april 2026</div>
              <div>updated · weekly</div>
            </div>
          </div>

          <div className="now">
            <div className="visual">
              <div className="halo" />
              <div className="vinyl">
                <div className="label-disc"><em>{now.artist}</em></div>
              </div>
            </div>
            <div className="detail">
              <div className="tag"><span className="pulse" />now playing</div>
              <h2><em>{now.track}</em></h2>
              <p className="artist">by {now.artist} · {now.album}, {now.year}</p>
              <p className="note">"{now.note}"</p>
              <div className="meta-row">
                <div className="item">
                  <span className="label k">duration</span>
                  <span className="v">{now.duration}</span>
                </div>
                <div className="item">
                  <span className="label k">year</span>
                  <span className="v">{now.year}</span>
                </div>
                <div className="item">
                  <span className="label k">found</span>
                  <span className="v italic">on a rainy tuesday</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* mixtapes */}
        <section className="section" data-screen-label="03 Mixtapes">
          <div className="section-head">
            <h2 className="heading"><span className="num">ii.</span><em>The Mixtapes</em></h2>
            <div className="meta">
              <div>vi volumes</div>
              <div>curated · 2025—2026</div>
            </div>
          </div>

          <div className="mixtapes">
            {mixtapes.map((m, i) => (
              <article
                key={m.id}
                className="mixtape"
                onClick={() => setSelectedMix(m)}
              >
                <div className="art">
                  <div className="halo-art" style={{ background: `radial-gradient(circle, ${m.color}, transparent 70%)` }} />
                  <Starfield seed={i * 37 + 11} color={m.color} />
                  <span className="tape-hole l" />
                  <span className="tape-hole r" />
                  <div className="inner">
                    <div className="roman">vol. {toRoman(i + 1)}</div>
                    <div className="t"><em>{m.title}</em></div>
                    <div className="mood">{m.mood}</div>
                  </div>
                  <div className="overlay-play">
                    <div className="circle">
                      <svg width="16" height="16" viewBox="0 0 16 16"><polygon points="3,2 13,8 3,14" fill="var(--ember)" /></svg>
                    </div>
                  </div>
                </div>
                <div className="caption">
                  <div className="title"><em>{m.title}</em></div>
                  <div className="date">{m.month} {String(m.year).slice(2)}</div>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* canon */}
        <section className="section" data-screen-label="04 Canon">
          <div className="section-head">
            <h2 className="heading"><span className="num">iii.</span><em>The Canon</em></h2>
            <div className="meta">
              <div>{favorites.length} tracks</div>
              <div>hover to preview · click to play</div>
            </div>
          </div>

          <div className="canon-intro">
            <p className="lede">
              Fifteen songs I would keep if I could only keep fifteen.
              They are arranged not by genre, or decade, but in the order
              they would play on a long slow afternoon.
            </p>
            <div className="aside">
              <div>span<span className="v italic">2010 — 2025</span></div>
              <div>lucky song<span className="v italic">grin · baynk</span></div>
              <div>longest<span className="v italic">6:18 · ameme</span></div>
              <div>
                on spotify
                <a
                  className="v italic"
                  href={window.CANON_PLAYLIST_URL}
                  target="_blank"
                  rel="noreferrer"
                  style={{ color: "var(--ember)", textDecoration: "none", borderBottom: "1px solid var(--ember)" }}
                >listen to the canon ↗</a>
              </div>
            </div>
          </div>

          <div className="tracklist">
            {favorites.map((t, i) => (
              <div
                key={i}
                className={`track ${previewingId === i ? "playing" : ""}`}
                onClick={() => setModalTrack(t)}
                onMouseEnter={() => setPreviewingId(i)}
                onMouseLeave={() => setPreviewingId(null)}
              >
                <div className="roman">{t.n}.</div>
                <div className="title"><em>{t.title}</em></div>
                <div className="artist">{t.artist}</div>
                <div className="tag">{t.tag}</div>
                <div className="dur">{t.duration}</div>
                <div className="play-icon">
                  {previewingId === i
                    ? <div className="eq"><span style={{height:'60%'}}/><span style={{height:'80%'}}/><span style={{height:'40%'}}/><span style={{height:'70%'}}/></div>
                    : <div className="dot" />
                  }
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* footer */}
        <footer className="footer">
          <div>a small corner of <em>stephie's world</em></div>
          <div className="mark">✶</div>
          <div><em>"music is the silence between the notes." — debussy</em></div>
        </footer>

      </div>

      <TrackModal
        track={modalTrack}
        open={!!modalTrack}
        onClose={() => setModalTrack(null)}
      />
      <MixtapeModal
        mix={selectedMix}
        open={!!selectedMix}
        onClose={() => setSelectedMix(null)}
      />
      <TweaksPanel
        tweaks={tweaks}
        setTweaks={setTweaks}
        visible={editVisible}
      />
    </>
  );
}

function toRoman(n) {
  const map = ["i","ii","iii","iv","v","vi","vii","viii","ix","x"];
  return map[n - 1] || String(n);
}

function MixtapeModal({ mix, open, onClose }) {
  React.useEffect(() => {
    const onKey = e => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);
  if (!mix) return null;
  return (
    <div className={`modal-scrim ${open ? "open" : ""}`} onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <button className="close" onClick={onClose}>close ×</button>
        <div className="eyebrow">a mixtape · {mix.month} {mix.year}</div>
        <h3><em>{mix.title}</em></h3>
        <div className="by"><em>{mix.subtitle}</em></div>

        {mix.playlistId ? (
          <div style={{ margin: "0 0 28px", borderRadius: 2, overflow: "hidden", boxShadow: "0 10px 40px rgba(42,26,24,0.15)" }}>
            <iframe
              title={`Spotify player — ${mix.title}`}
              src={`https://open.spotify.com/embed/playlist/${mix.playlistId}?utm_source=generator&theme=0`}
              width="100%"
              height="352"
              frameBorder="0"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
              loading="lazy"
              style={{ display: "block", border: 0 }}
            />
          </div>
        ) : (
          <div className="player">
            <button className="play-btn" aria-label="play">▶</button>
            <div className="bar" style={{ "--progress": "0%" }} />
            <span className="time">00:00</span>
            <span className="preview-note">{mix.trackCount} tracks</span>
          </div>
        )}

        <p className="quote" style={{ marginBottom: 24 }}>
          {mix.mood} — a mixtape for the hours when you don't quite know what
          to do with yourself. Let it decide.
        </p>

        {mix.playlistUrl && (
          <a
            href={mix.playlistUrl}
            target="_blank"
            rel="noreferrer"
            style={{
              fontFamily: "var(--mono)",
              fontSize: 10,
              letterSpacing: "0.22em",
              textTransform: "uppercase",
              color: "var(--ember)",
              textDecoration: "none",
              borderBottom: "1px solid var(--ember)",
              paddingBottom: 3,
            }}
          >open in spotify ↗</a>
        )}
      </div>
    </div>
  );
}

Object.assign(window, { App, MixtapeModal });
