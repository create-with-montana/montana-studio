// Hero cutout: paints the hero photo inside the frosted letters, aligned with
// the photo behind the glass, so the letters read as a clear window.
(function () {
  var hero = document.querySelector('.hero');
  var word = document.querySelector('.split-head .fogged');
  if (!hero || !word || !CSS.supports('(background-clip: text) or (-webkit-background-clip: text)')) return;
  var IMG_W = 2200, IMG_H = 1467; // images/hero-library.jpg

  function align() {
    var h = hero.getBoundingClientRect(), w = word.getBoundingClientRect();
    var scale = Math.max(h.width / IMG_W, h.height / IMG_H); // background-size: cover
    var iw = IMG_W * scale, ih = IMG_H * scale;
    var pos = getComputedStyle(hero).backgroundPosition.split(' ').map(parseFloat); // percentages
    var x = (h.width - iw) * pos[0] / 100 + (h.left - w.left);
    var y = (h.height - ih) * pos[1] / 100 + (h.top - w.top);
    word.style.backgroundSize = iw + 'px ' + ih + 'px';
    word.style.backgroundPosition = x + 'px ' + y + 'px';
    word.classList.add('cutout');
  }

  align();
  window.addEventListener('resize', align);
  if (document.fonts) document.fonts.ready.then(align);
})();
