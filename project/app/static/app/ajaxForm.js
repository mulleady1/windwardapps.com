$(document).ready(function() {
  $('form[data-ajax-form]').each(function(i, el) {
    $(el).on('submit', function(e) {
      e.preventDefault();
      var btn = $(el).find('button[type="submit"]')[0];
      var text = btn.textContent;
      var successUrl = el.dataset.successUrl;
      btn.disabled = true;
      btn.textContent = 'Processing...';
      $.post({
        url: $(el).attr('action'),
        data: $(el).serialize()
      }).then(function(data) {
        console.log('success: ', data);
        btn.disabled = false;
        btn.textContent = text;

        if (successUrl) {
          window.location = el.dataset.successUrl;
        } else if (el._onSuccess) {
          el._onSuccess();
        }
      }).catch(function(xhr) {
        var data = xhr.responseJSON;
        console.log('error: ', data);
        btn.disabled = false;
        btn.textContent = text;
        $(el).find('.message').html(data.msg);

        var onInput = function() {
          $(el).find('.message').html('');
          $(el).find('input').off('input', onInput);
        };

        $(el).find('input').on('input', onInput);
      });
    });
  });
});
