// Services: turns each "included" list into a one-at-a-time slider with a
// quiet arrow and a progress hairline. Without JS the list shows inline.
(function () {
  var arrow = '<svg viewBox="0 0 26 10" aria-hidden="true"><path d="M0 5h24M20 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1"/></svg>';

  document.querySelectorAll('.svc .incl').forEach(function (list) {
    var names = Array.prototype.map.call(list.children, function (li) { return li.textContent; });
    if (!names.length) return;
    var title = list.closest('.svc').querySelector('h3').textContent;

    var box = document.createElement('div');
    box.className = 'incl-slider';
    box.setAttribute('role', 'group');
    box.setAttribute('aria-label', 'Included in ' + title);
    box.innerHTML = '<span class="stage" aria-live="polite"></span>' +
      '<button class="next" type="button" aria-label="Next included item">' + arrow + '</button>' +
      '<span class="bar" aria-hidden="true"><span></span></span>';

    var stage = box.querySelector('.stage'), fill = box.querySelector('.bar span');
    var items = names.map(function (n) {
      var s = document.createElement('span'); s.className = 'item'; s.textContent = n; stage.appendChild(s); return s;
    });
    var i = 0;
    function show(next) {
      items[i].classList.remove('is-on'); items[i].classList.add('is-out');
      var leaving = items[i];
      setTimeout(function () { leaving.classList.remove('is-out'); }, 550);
      i = next;
      items[i].classList.add('is-on');
      fill.style.width = ((i + 1) / items.length * 100) + '%';
    }
    items[0].classList.add('is-on');
    fill.style.width = (100 / items.length) + '%';
    box.querySelector('.next').addEventListener('click', function () { show((i + 1) % items.length); });

    list.hidden = true;
    list.after(box);
  });
})();
