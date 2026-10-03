// Mobile menu: the Menu button opens a full-screen frosted panel with the same
// links as the desktop nav. Closes on a link, the Close button or Escape.
(function () {
  var btn = document.querySelector('.nav .menu'), nav = btn && btn.parentNode;
  var list = nav && nav.querySelector('ul'), mark = nav && nav.querySelector('.wordmark');
  if (!list || !mark) return;

  var panel = document.createElement('div');
  panel.className = 'mobile-menu'; panel.id = 'site-menu'; panel.hidden = true;
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'true'); panel.setAttribute('aria-label', 'Menu');
  panel.innerHTML = '<div class="mm-top">' + mark.outerHTML + '<button class="menu mm-close" type="button">Close</button></div>'
    + '<nav aria-label="Menu"><ul>' + list.innerHTML + '</ul></nav>'
    + '<a class="mm-mail" href="mailto:montana@createwithmontana.com">montana@createwithmontana.com</a>';
  document.body.appendChild(panel);
  var close = panel.querySelector('.mm-close');
  btn.setAttribute('aria-controls', 'site-menu'); btn.setAttribute('aria-expanded', 'false');

  function open() {
    panel.hidden = false; document.documentElement.classList.add('menu-open');
    btn.setAttribute('aria-expanded', 'true');
    requestAnimationFrame(function () { panel.classList.add('open'); close.focus(); });
  }
  function shut(keepFocus) {
    panel.classList.remove('open'); document.documentElement.classList.remove('menu-open');
    btn.setAttribute('aria-expanded', 'false');
    setTimeout(function () { panel.hidden = true; }, 350);
    if (!keepFocus) btn.focus();
  }

  btn.addEventListener('click', open);
  close.addEventListener('click', function () { shut(); });
  panel.querySelectorAll('nav a').forEach(function (a) { a.addEventListener('click', function () { shut(true); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) shut(); });
  window.addEventListener('resize', function () { if (!panel.hidden && window.innerWidth > 760) shut(true); });
})();
