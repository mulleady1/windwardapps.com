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
        if (!data) {
          var $msg = $('<div class="message">An error occurred. Please try again later.</div>');
          $(el).prepend($msg);
          setTimeout(function() {
            $msg.css('transition', 'max-height 150ms');
            $msg.css('max-height', 0);
            setTimeout(function() {
              $msg.remove();
            }, 250);
          }, 5000);
        } else if (data.msg) {
          var $message = $(el).find('.message');
          $message.html(data.msg);
          $(el).find('input, textarea').one('input', function() {
            $message.html('');
          });
        } else if (data.errors) {
          Object.keys(data.errors).forEach(key => {
            var msg = data.errors[key][0],
              $msg = $('<div class="field-message">' + msg + '</div>'),
              $input = $(el).find('[name="' + key + '"]');

            $input.parent().append($msg);
            $input.one('input', function() {
              $msg.remove();
            });
          });
        }
      });
    });
  });
});
