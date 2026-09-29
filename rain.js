// Fine, slanted rain over the page. Mostly cream, now and then a red streak
// catching a sign. Skipped entirely for reduced-motion users.
function startRain(canvas, density) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var ctx = canvas.getContext('2d');
  var drops = [];
  var w, h, dpr;

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = canvas.clientWidth;
    h = canvas.clientHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var n = Math.round((w * h) / 9000 * (density || 1));
    drops = [];
    for (var i = 0; i < n; i++) drops.push(spawn(true));
  }

  function spawn(anywhere) {
    return {
      x: Math.random() * (w + 200) - 100,
      y: anywhere ? Math.random() * h : -30,
      len: 8 + Math.random() * 18,
      speed: 5 + Math.random() * 7,
      alpha: 0.04 + Math.random() * 0.12,
      red: Math.random() < 0.12
    };
  }

  function frame() {
    ctx.clearRect(0, 0, w, h);
    ctx.lineWidth = 0.7;
    for (var i = 0; i < drops.length; i++) {
      var d = drops[i];
      ctx.strokeStyle = d.red
        ? 'rgba(255,45,74,' + (d.alpha * 1.6) + ')'
        : 'rgba(239,228,214,' + d.alpha + ')';
      ctx.beginPath();
      ctx.moveTo(d.x, d.y);
      ctx.lineTo(d.x - d.len * 0.18, d.y + d.len);
      ctx.stroke();
      d.y += d.speed;
      d.x -= d.speed * 0.18;
      if (d.y > h) drops[i] = spawn(false);
    }
    requestAnimationFrame(frame);
  }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(frame);
}
