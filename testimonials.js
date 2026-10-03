// Testimonials: stacks the reviews in one spot and cross-fades between them,
// with quiet arrows, a sliding hairline and swipe on touch. Without JS they show in a column.
(function () {
  var wrap = document.querySelector('.reviews');
  if (!wrap) return;
  var slides = wrap.querySelectorAll('.review');
  if (slides.length < 2) return;
  var arrow = '<svg viewBox="0 0 26 10" aria-hidden="true"><path d="M0 5h24M20 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1"/></svg>';

  var nav = document.createElement('div');
  nav.className = 'review-nav';
  nav.innerHTML = '<button class="prev" type="button" aria-label="Previous testimonial">' + arrow + '</button>' +
    '<span class="bar" aria-hidden="true"><span></span></span>' +
    '<button class="next" type="button" aria-label="Next testimonial">' + arrow + '</button>';
  var fill = nav.querySelector('.bar span');
  fill.style.width = (100 / slides.length) + '%';

  var i = 0;
  function show(n) {
    slides[i].classList.remove('is-on'); slides[i].setAttribute('aria-hidden', 'true');
    i = (n + slides.length) % slides.length;
    slides[i].classList.add('is-on'); slides[i].removeAttribute('aria-hidden');
    fill.style.left = (i * 100 / slides.length) + '%';
  }
  slides.forEach(function (s, n) { s.setAttribute('aria-roledescription', 'slide'); s.setAttribute('aria-label', (n + 1) + ' of ' + slides.length); if (n) s.setAttribute('aria-hidden', 'true'); });
  slides[0].classList.add('is-on');
  fill.style.left = '0%';
  wrap.classList.add('is-slider');
  wrap.setAttribute('aria-roledescription', 'carousel');
  wrap.after(nav);

  nav.querySelector('.prev').addEventListener('click', function () { show(i - 1); });
  nav.querySelector('.next').addEventListener('click', function () { show(i + 1); });

  var x0 = null;
  wrap.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  wrap.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
  });
})();
