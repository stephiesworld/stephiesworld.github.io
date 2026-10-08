// Fine, slanted rain over the page. Mostly cream, now and then a red streak
// catching a sign. Skipped entirely for reduced-motion users.
//
// startRain(canvas, density) returns a control: set('rain' | 'snow' | 'none', density)
// lets a page match the sky to the real weather.
function startRain(canvas, density) {
  var noop = { set: function () {} };
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return noop;
  var ctx = canvas.getContext('2d');
  var drops = [];
  var w, h, dpr;
  var kind = 'rain';
  var amount = density == null ? 1 : density;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth;
    h = canvas.clientHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    fill();
  }

  function fill() {
    var per = kind === 'snow' ? 14000 : 9000;
    var n = kind === 'none' ? 0 : Math.round((w * h) / per * amount);
    drops = [];
    for (var i = 0; i < n; i++) drops.push(spawn(true));
  }

  function spawn(anywhere) {
    if (kind === 'snow') {
      return {
        x: Math.random() * w,
        y: anywhere ? Math.random() * h : -10,
        r: 0.6 + Math.random() * 1.6,
        speed: 0.4 + Math.random() * 0.9,
        sway: Math.random() * 6.28,
        alpha: 0.15 + Math.random() * 0.35
      };
    }
    return {
      x: Math.random() * (w + 200) - 100,
      y: anywhere ? Math.random() * h : -30,
      len: 8 + Math.random() * 18,
      speed: 5 + Math.random() * 7,
      alpha: 0.04 + Math.random() * 0.12,
      red: Math.random() < 0.12
    };
  }

  function frame(t) {
    ctx.clearRect(0, 0, w, h);
    for (var i = 0; i < drops.length; i++) {
      var d = drops[i];
      if (kind === 'snow') {
        ctx.fillStyle = 'rgba(239,228,214,' + d.alpha + ')';
        ctx.beginPath();
        ctx.arc(d.x + Math.sin(t / 1400 + d.sway) * 8, d.y, d.r, 0, 6.283);
        ctx.fill();
        d.y += d.speed;
      } else {
        ctx.lineWidth = 0.7;
        ctx.strokeStyle = d.red
          ? 'rgba(255,122,146,' + (d.alpha * 1.6) + ')'
          : 'rgba(239,228,214,' + d.alpha + ')';
        ctx.beginPath();
        ctx.moveTo(d.x, d.y);
        ctx.lineTo(d.x - d.len * 0.18, d.y + d.len);
        ctx.stroke();
        d.y += d.speed;
        d.x -= d.speed * 0.18;
      }
      if (d.y > h) drops[i] = spawn(false);
    }
    requestAnimationFrame(frame);
  }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(frame);

  return {
    set: function (k, d) {
      kind = k;
      if (d != null) amount = d;
      fill();
    }
  };
}
