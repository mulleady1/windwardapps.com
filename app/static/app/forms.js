/* Mounts hCaptcha widgets, including ones htmx swaps in later, and enables the
   form's submit button once the captcha passes. api.js is loaded with
   render=explicit&onload=wwaCaptchaReady (see base.html). */
(function () {
  function enableSubmit(widget) {
    var form = widget.closest('form');
    var button = form && form.querySelector('[type="submit"]');
    if (button) button.disabled = false;
  }

  function mountOne(el) {
    if (el.dataset.mounted || !window.hcaptcha) return;
    el.dataset.mounted = '1';
    hcaptcha.render(el, {
      sitekey: el.dataset.sitekey,
      callback: function () { enableSubmit(el); },
      'expired-callback': function () {
        var form = el.closest('form');
        var button = form && form.querySelector('[type="submit"]');
        if (button) button.disabled = true;
      }
    });
  }

  function mount(root) {
    if (root.nodeType !== 1) return;
    if (root.matches('.h-captcha')) mountOne(root);
    root.querySelectorAll('.h-captcha').forEach(mountOne);
  }

  window.wwaMountCaptchas = mount;
  if (window.__captchaReady) mount(document.documentElement);

  new MutationObserver(function (mutations) {
    mutations.forEach(function (m) { m.addedNodes.forEach(mount); });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
