/* Comportements minimaux reproduits : fil d'info et slider "A la une". Aucun chargement différé. */
(function () {
  function cycle(items, delay, prevBtn, nextBtn, pauseBtn) {
    var i = 0, timer = null;
    function show(n) { items[i].classList.remove('on'); i = (n + items.length) % items.length; items[i].classList.add('on'); }
    function start() { timer = setInterval(function () { show(i + 1); }, delay); }
    function stop() { clearInterval(timer); timer = null; }
    if (prevBtn) prevBtn.onclick = function () { show(i - 1); };
    if (nextBtn) nextBtn.onclick = function () { show(i + 1); };
    if (pauseBtn) pauseBtn.onclick = function () { timer ? stop() : start(); };
    start();
  }
  document.addEventListener('DOMContentLoaded', function () {
    cycle(document.querySelectorAll('#fil_info_texte li'), 5000,
      document.getElementById('precedent'), document.getElementById('suivant'), document.getElementById('pause'));
    cycle(document.querySelectorAll('#slider .slide'), 8000);
  });
})();
