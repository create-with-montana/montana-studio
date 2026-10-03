// Inquiry form: sends through FormSubmit without leaving the page and shows a
// thank-you note. Without JS the form posts normally to the same address.
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
      .then(function () {
        form.reset();
        note.textContent = 'Thank you. We will be in touch within two business days.';
      })
      .catch(function () {
        note.textContent = 'Something went wrong. Please email montana@createwithmontana.com.';
      })
      .finally(function () { button.disabled = false; });
  });
})();
