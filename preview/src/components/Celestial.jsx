// HeroConstellation.jsx — celestial SVG for hero

function HeroConstellation() {
  // octagon node positions (like the parent site)
  const cx = 410, cy = 260, r = 220;
  const nodes = [];
  for (let i = 0; i < 8; i++) {
    const a = (Math.PI * 2 * i) / 8 - Math.PI / 2;
    nodes.push({ x: cx + Math.cos(a) * r, y: cy + Math.sin(a) * r });
  }
  // inner stars
  const inner = [];
  for (let i = 0; i < 14; i++) {
    const a = Math.random() * Math.PI * 2;
    const rr = 40 + Math.random() * 130;
    inner.push({ x: cx + Math.cos(a) * rr, y: cy + Math.sin(a) * rr, r: 0.8 + Math.random() * 1.2 });
  }
  return (
    <svg viewBox="0 0 820 520" fill="none">
      <defs>
        <radialGradient id="node-glow">
          <stop offset="0%" stopColor="var(--ember)" stopOpacity="0.9" />
          <stop offset="60%" stopColor="var(--ember)" stopOpacity="0.2" />
          <stop offset="100%" stopColor="var(--ember)" stopOpacity="0" />
        </radialGradient>
      </defs>
      {/* octagon path */}
      <polygon
        points={nodes.map(n => `${n.x},${n.y}`).join(" ")}
        stroke="var(--ember)"
        strokeOpacity="0.35"
        strokeWidth="0.5"
      />
      {/* inner circles */}
      <circle cx={cx} cy={cy} r="110" stroke="var(--ember)" strokeOpacity="0.25" strokeWidth="0.5" />
      <circle cx={cx} cy={cy} r="60" stroke="var(--ember)" strokeOpacity="0.2" strokeWidth="0.5" />
      {/* outer nodes with glow */}
      {nodes.map((n, i) => (
        <g key={i}>
          <circle cx={n.x} cy={n.y} r="16" fill="url(#node-glow)" className="breathe" style={{ animationDelay: `${i * 0.4}s` }} />
          <circle cx={n.x} cy={n.y} r="2" fill="var(--ember)" />
        </g>
      ))}
      {/* inner stars */}
      {inner.map((n, i) => (
        <circle key={`s${i}`} cx={n.x} cy={n.y} r={n.r} fill="var(--ember)" opacity={0.4 + Math.random() * 0.4} />
      ))}
      {/* center heart-like mark */}
      <g transform={`translate(${cx} ${cy})`}>
        <circle r="24" fill="url(#node-glow)" className="breathe" />
        <circle r="3.5" fill="var(--ember)" />
      </g>
    </svg>
  );
}

// Starfield inside mixtape art
function Starfield({ seed = 1, color = "#8b1e2f" }) {
  const stars = React.useMemo(() => {
    const arr = [];
    let s = seed;
    const rnd = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
    for (let i = 0; i < 30; i++) {
      arr.push({ x: rnd() * 100, y: rnd() * 100, r: rnd() * 0.8 + 0.2, o: rnd() * 0.6 + 0.2 });
    }
    return arr;
  }, [seed]);
  return (
    <svg className="starfield" viewBox="0 0 100 100" preserveAspectRatio="none">
      {stars.map((s, i) => (
        <circle key={i} cx={s.x} cy={s.y} r={s.r} fill={color} opacity={s.o} />
      ))}
    </svg>
  );
}

Object.assign(window, { HeroConstellation, Starfield });
