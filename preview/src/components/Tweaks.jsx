// Tweaks.jsx — in-page tweaks panel

function TweaksPanel({ tweaks, setTweaks, visible }) {
  const set = (k, v) => {
    const next = { ...tweaks, [k]: v };
    setTweaks(next);
    try {
      window.parent.postMessage({ type: "__edit_mode_set_keys", edits: { [k]: v } }, "*");
    } catch (e) {}
  };

  const palettes = [
    { id: "cream", label: "Cream", swatch: "#e8c5bd" },
    { id: "ink",   label: "Ink",   swatch: "#1a1513" },
    { id: "moss",  label: "Moss",  swatch: "#c5cfa8" },
  ];

  return (
    <div className={`tweaks-panel ${visible ? "open" : ""}`}>
      <h4>Tweaks</h4>

      <div className="row">
        <label>palette</label>
        <div className="swatches">
          {palettes.map(p => (
            <button
              key={p.id}
              className={`swatch ${tweaks.palette === p.id ? "active" : ""}`}
              style={{ background: p.swatch }}
              onClick={() => set("palette", p.id)}
              title={p.label}
              aria-label={p.label}
            />
          ))}
        </div>
      </div>

      <div className="row">
        <label>grid density</label>
        <div className="seg">
          {["2", "3", "4"].map(d => (
            <button
              key={d}
              className={tweaks.density === d ? "active" : ""}
              onClick={() => set("density", d)}
            >{d}</button>
          ))}
        </div>
      </div>

      <div className="row">
        <label>motion</label>
        <div className="seg">
          {["on", "off"].map(m => (
            <button
              key={m}
              className={tweaks.motion === m ? "active" : ""}
              onClick={() => set("motion", m)}
            >{m}</button>
          ))}
        </div>
      </div>

      <div className="row">
        <label>grain</label>
        <input
          type="range"
          min="0" max="0.15" step="0.01"
          value={tweaks.grain}
          onChange={e => set("grain", parseFloat(e.target.value))}
        />
      </div>
    </div>
  );
}

Object.assign(window, { TweaksPanel });
