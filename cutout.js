// Glass cutouts: paints the section photo inside the frosted letters, aligned
// with the photo behind the glass, so the letters read as a clear window.
// Used by the hero (CLARITY) and the inquiry section (Clarity.).
(function () {
  if (!CSS.supports('(background-clip: text) or (-webkit-background-clip: text)')) return;
  var sets = [
    { frame: '.hero', word: '.split-head .fogged', on: 'cutout', w: 2200, h: 1467 },       // images/hero-library.jpg
    { frame: '.inquire', word: '.look .cut', on: 'cutout', w: 1650, h: 2200 }  // images/inquire-stairs.jpg
  ];

  function align(c) {
    var frame = document.querySelector(c.frame), word = frame && frame.querySelector(c.word);
    if (!word) return;
    var f = frame.getBoundingClientRect(), w = word.getBoundingClientRect();
    var scale = Math.max(f.width / c.w, f.height / c.h); // background-size: cover
    var iw = c.w * scale, ih = c.h * scale;
    var pos = getComputedStyle(frame).backgroundPosition.split(' ').map(parseFloat); // percentages
    word.style.backgroundSize = iw + 'px ' + ih + 'px';
    word.style.backgroundPosition = ((f.width - iw) * pos[0] / 100 + f.left - w.left) + 'px ' + ((f.height - ih) * pos[1] / 100 + f.top - w.top) + 'px';
    word.classList.add(c.on);
  }

  function all() { sets.forEach(align); }
  all();
  window.addEventListener('resize', all);
  if (document.fonts) document.fonts.ready.then(all);
})();
