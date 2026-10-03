// Inquiry form: sends through FormSubmit (which emails each inquiry to
// montana@createwithmontana.com), then opens the thank-you page. Without JS, or
// before the form is activated, it posts normally and FormSubmit redirects (_next).
(function () {
  var form = document.querySelector('.inquiry-form');
  if (!form || !window.fetch) return;
  var note = form.querySelector('.form-note'), button = form.querySelector('button');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form._honey.value) return;
    button.disabled = true; note.textContent = 'Sending…';
    fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
      method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form)
    }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        if (String(d.success) !== 'true') throw new Error(d.message || '');
        window.location.href = '/thank-you';
      })
      .catch(function (err) {
        // Until the form is activated, FormSubmit wants one normal (non-AJAX) send, which
        // shows its own page and emails the activation link to montana@createwithmontana.com
        if (/activat/i.test(err.message)) { note.textContent = 'One moment…'; form.submit(); return; }
        note.textContent = 'Something went wrong. Please email montana@createwithmontana.com.';
      })
      .finally(function () { button.disabled = false; });
  });
})();
