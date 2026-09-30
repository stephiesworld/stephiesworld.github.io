// A secret: type 29 anywhere on the site. The globe turns to where the book began.
(function () {
  var home = new URL('index.html', document.currentScript.src).href;
  var typed = '';
  document.addEventListener('keydown', function (e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var t = e.target;
    if (t && (t.isContentEditable || /^(input|textarea|select)$/i.test(t.tagName))) return;
    typed = (typed + e.key).slice(-2);
    if (typed !== '29') return;
    typed = '';
    if (typeof window.__twentyNine === 'function') window.__twentyNine();
    else location.href = home + '#29';
  });
})();
