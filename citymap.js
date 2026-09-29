// Shared night map for the city pages. Each page calls cityMap({...}) with its places.
//
// config: {
//   tz, bearing, home: { center, zoom, pitch }, bounds,
//   groups: [{ id, label, big, labels: 'always'|'hover', tagsLabel }],
//   places: [{ id, group, name, lngLat, address, category, role, years, copy, did: [], tags: [], links: [{ href, label }], route }]
// }
// Deep links: page.html#guide opens a tab, page.html#placeid opens a place.
function cityMap(cfg) {
  var mobile = window.innerWidth < 760;
  var PAD = mobile ? { top: 0, bottom: 200, left: 0, right: 0 } : { top: 0, bottom: 0, left: 320, right: 0 };
  var PAD_CARD = mobile ? { top: 0, bottom: 320, left: 0, right: 0 } : { top: 0, bottom: 0, left: 320, right: 420 };
  var HOME = Object.assign({ bearing: cfg.bearing || 0, padding: PAD }, cfg.home);
  if (mobile) HOME.zoom -= 0.8;

  // ─── Night style over OpenFreeMap vector tiles ───
  var roadMajor = ['in', ['get', 'class'], ['literal', ['motorway', 'trunk', 'primary', 'secondary']]];
  var roadMinor = ['in', ['get', 'class'], ['literal', ['tertiary', 'minor', 'service']]];
  var name = ['upcase', ['coalesce', ['get', 'name:en'], ['get', 'name']]];
  var STYLE = {
    version: 8,
    glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
    // Keep the light neutral: MapLibre adds (1 - light colour) as ambient, so a red light turns roofs teal
    light: { anchor: 'viewport', color: '#ffffff', intensity: 0.2, position: [1.4, 210, 35] },
    sources: { omt: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' } },
    layers: [
      { id: 'bg', type: 'background', paint: { 'background-color': '#08070a' } },
      { id: 'park', type: 'fill', source: 'omt', 'source-layer': 'park', paint: { 'fill-color': '#0c0b0d' } },
      { id: 'water', type: 'fill', source: 'omt', 'source-layer': 'water', paint: { 'fill-color': '#040509' } },
      { id: 'shore-glow', type: 'line', source: 'omt', 'source-layer': 'water',
        paint: { 'line-color': '#ffb15c', 'line-opacity': 0.18, 'line-blur': 4, 'line-width': ['interpolate', ['linear'], ['zoom'], 11, 2, 16, 8] } },
      { id: 'shore', type: 'line', source: 'omt', 'source-layer': 'water',
        paint: { 'line-color': '#ffb15c', 'line-opacity': 0.4, 'line-width': 0.6 } },
      { id: 'road-minor', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: roadMinor,
        paint: { 'line-color': '#4a1620', 'line-opacity': 0.55, 'line-width': ['interpolate', ['linear'], ['zoom'], 12, 0.3, 16, 1.6] } },
      { id: 'road-major-glow', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: roadMajor,
        paint: { 'line-color': '#ff2d4a', 'line-opacity': 0.1, 'line-blur': 5, 'line-width': ['interpolate', ['linear'], ['zoom'], 11, 3, 16, 14] } },
      { id: 'road-major', type: 'line', source: 'omt', 'source-layer': 'transportation', filter: roadMajor,
        paint: { 'line-color': '#c8354c', 'line-opacity': 0.5, 'line-width': ['interpolate', ['linear'], ['zoom'], 11, 0.4, 16, 1.6] } },
      { id: 'buildings', type: 'fill-extrusion', source: 'omt', 'source-layer': 'building', minzoom: 12,
        paint: {
          'fill-extrusion-color': ['interpolate', ['linear'], ['coalesce', ['get', 'render_height'], 0], 0, '#0b0609', 80, '#13070d', 250, '#1e0912'],
          'fill-extrusion-height': ['coalesce', ['get', 'render_height'], 0],
          'fill-extrusion-base': ['coalesce', ['get', 'render_min_height'], 0],
          'fill-extrusion-opacity': 0.92
        } },
      { id: 'water-name', type: 'symbol', source: 'omt', 'source-layer': 'water_name',
        filter: ['in', ['get', 'class'], ['literal', ['river', 'bay', 'strait', 'sea', 'ocean']]],
        layout: { 'text-field': name, 'text-font': ['Noto Sans Italic'], 'text-size': 10, 'text-letter-spacing': 0.4 },
        paint: { 'text-color': 'rgba(255,177,92,0.35)' } },
      { id: 'hood', type: 'symbol', source: 'omt', 'source-layer': 'place',
        filter: ['in', ['get', 'class'], ['literal', ['neighbourhood', 'suburb', 'quarter']]],
        layout: { 'text-field': name, 'text-font': ['Noto Sans Regular'], 'text-size': 9, 'text-letter-spacing': 0.35 },
        paint: { 'text-color': 'rgba(239,228,214,0.22)', 'text-halo-color': '#08070a', 'text-halo-width': 1.2 } }
    ]
  };

  var map = new maplibregl.Map({
    container: 'map',
    style: STYLE,
    center: HOME.center, zoom: HOME.zoom - 1.2, pitch: 20, bearing: HOME.bearing - 20,
    attributionControl: { compact: true },
    maxBounds: cfg.bounds
  });

  var groups = {};
  cfg.groups.forEach(function (g) { groups[g.id] = g; });
  var byId = {};
  cfg.places.forEach(function (p) { byId[p.id] = p; });

  map.on('load', function () {
    document.getElementById('map').classList.add('ready');
    map.flyTo(Object.assign({ duration: 4200, essential: true }, HOME));

    // Routes (runs), lit like a strip of sodium lamps
    cfg.places.filter(function (p) { return p.route; }).forEach(function (p) {
      map.addSource('route-' + p.id, { type: 'geojson', data: { type: 'Feature', geometry: { type: 'LineString', coordinates: p.route } } });
      map.addLayer({ id: 'route-glow-' + p.id, type: 'line', source: 'route-' + p.id, layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': '#ffb15c', 'line-opacity': 0.3, 'line-blur': 6, 'line-width': 10 } });
      map.addLayer({ id: 'route-' + p.id, type: 'line', source: 'route-' + p.id, layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: { 'line-color': '#ffb15c', 'line-opacity': 0.75, 'line-width': 1.4, 'line-dasharray': [2, 2] } });
    });
  });

  // ─── Markers ───
  var markers = {};
  cfg.places.forEach(function (p) {
    if (!p.lngLat) return;
    var g = groups[p.group];
    var el = document.createElement('div');
    el.className = 'mk g-' + p.group + (g.big ? ' big' : '');
    el.innerHTML = '<span class="mk-dot"></span><span class="mk-label">' + p.name + '</span>';
    el.addEventListener('click', function (e) { e.stopPropagation(); select(p.id); });
    markers[p.id] = { el: el, place: p, marker: new maplibregl.Marker({ element: el }).setLngLat(p.lngLat).addTo(map) };
  });

  // ─── Tabs & list ───
  var tabsEl = document.getElementById('tabs');
  var listEl = document.getElementById('list');
  var activeGroup = null;

  if (cfg.groups.length > 1) {
    cfg.groups.forEach(function (g) {
      var b = document.createElement('button');
      b.className = 'tab hud g-' + g.id;
      b.dataset.group = g.id;
      b.innerHTML = '<span class="dot"></span>' + g.label;
      b.addEventListener('click', function () { showGroup(g.id); });
      tabsEl.appendChild(b);
    });
  } else {
    tabsEl.style.display = 'none';
  }

  function showGroup(id) {
    activeGroup = id;
    var g = groups[id];
    tabsEl.querySelectorAll('.tab').forEach(function (t) { t.classList.toggle('active', t.dataset.group === id); });
    listEl.className = 'list g-' + id;
    listEl.innerHTML = '';
    var n = 0, lastCat = null;
    cfg.places.filter(function (p) { return p.group === id; }).forEach(function (p) {
      if (p.category && p.category !== lastCat) {
        lastCat = p.category;
        var c = document.createElement('p');
        c.className = 'list-cat hud';
        c.textContent = p.category;
        listEl.appendChild(c);
      }
      var b = document.createElement('button');
      b.className = 'item' + (g.compact ? ' compact' : '') + (p.id === current ? ' active' : '');
      b.dataset.id = p.id;
      b.innerHTML = (g.compact ? '' : '<span class="n">' + String(++n).padStart(2, '0') + '</span>') +
        '<span>' + p.name + '</span>' + (p.years ? '<span class="yr">' + p.years.split(/\s*[–-]\s*/)[0] + '</span>' : '');
      b.addEventListener('click', function () { select(p.id); });
      listEl.appendChild(b);
    });
    listEl.scrollTop = 0;
    listEl.scrollLeft = 0;
    paintMarkers();
  }

  function paintMarkers() {
    Object.keys(markers).forEach(function (k) {
      var m = markers[k], g = groups[m.place.group];
      var inGroup = m.place.group === activeGroup;
      m.el.classList.toggle('muted', !inGroup && !current);
      m.el.classList.toggle('show-label', inGroup && g.labels === 'always' && !current);
      m.el.classList.toggle('active', k === current);
      m.el.classList.toggle('dim', !!current && k !== current);
      m.el.style.zIndex = k === current ? 3 : inGroup ? 2 : 1;
    });
  }

  // ─── Detail card ───
  var card = document.getElementById('card');
  var current = null;

  function $(id) { return document.getElementById(id); }
  function show(el, html) { el.innerHTML = html || ''; el.style.display = html ? '' : 'none'; }

  function select(id) {
    var p = byId[id], g = groups[p.group];
    current = id;
    if (activeGroup !== p.group) showGroup(p.group);
    listEl.querySelectorAll('.item').forEach(function (b) { b.classList.toggle('active', b.dataset.id === id); });
    var activeItem = listEl.querySelector('.item.active');
    if (activeItem) activeItem.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' });
    paintMarkers();

    card.className = 'card open g-' + p.group;
    $('cKicker').innerHTML = '<i>&#9632;</i> &nbsp;' + g.label + (p.category ? ' &middot; ' + p.category : '');
    $('cName').innerHTML = p.name;
    show($('cRole'), [p.role, p.years].filter(Boolean).join('<br>'));
    show($('cAddr'), [p.address, p.note].filter(Boolean).join('<br>'));
    show($('cCopy'), p.copy);
    show($('cDid'), (p.did || []).map(function (d) { return '<li>' + d + '</li>'; }).join(''));
    var tags = p.tags || [];
    $('cTagsLabel').style.display = tags.length ? '' : 'none';
    $('cTagsLabel').textContent = g.tagsLabel || 'for';
    $('cTags').innerHTML = tags.map(function (t) { return '<span class="tag">' + t + '</span>'; }).join('');
    if ($('cLinks')) show($('cLinks'), (p.links || []).map(function (l) { return '<a href="' + l.href + '">' + l.label + ' &rarr;</a>'; }).join(''));
    card.scrollTop = 0;

    if (p.lngLat) {
      map.flyTo({
        center: p.lngLat, zoom: p.zoom || (p.route ? 13.8 : 15.2), pitch: 56, bearing: HOME.bearing + 12,
        padding: PAD_CARD, duration: 2400, essential: true
      });
    }
    history.replaceState(null, '', '#' + id);
  }

  function deselect() {
    if (!current) return;
    current = null;
    card.classList.remove('open');
    listEl.querySelectorAll('.item').forEach(function (b) { b.classList.remove('active'); });
    paintMarkers();
    map.flyTo(Object.assign({ duration: 2400, essential: true }, HOME));
    history.replaceState(null, '', '#' + activeGroup);
  }

  $('cardClose').addEventListener('click', deselect);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') deselect(); });
  map.on('click', deselect);

  // ─── Start ───
  var hash = location.hash.slice(1);
  showGroup(groups[hash] ? hash : byId[hash] ? byId[hash].group : cfg.groups[0].id);
  if (byId[hash]) map.once('load', function () { setTimeout(function () { select(hash); }, 4300); });

  if ($('clock')) {
    var tick = function () {
      $('clock').textContent = new Intl.DateTimeFormat('en-GB', { timeZone: cfg.tz, hour: '2-digit', minute: '2-digit' }).format(new Date());
    };
    tick();
    setInterval(tick, 30000);
  }

  return map;
}
