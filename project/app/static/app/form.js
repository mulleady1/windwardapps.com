$(document).ready(function() {
  function setState(el) {
    $(el).parent().removeClass('focus');
    if (el.value.trim()) {
      $(el).parent().addClass('has-value');
    } else {
      $(el).parent().removeClass('has-value');
    }
  }

  $('form input, form textarea').each(function(i, el) {
    setState(el);

    $(el)
      .on('focus', function() {
        $(el).parent().addClass('focus');
      })
      .on('blur', function() {
        setState(el);
      });
  });

  $('form > p label').each(function(i, el) {
    $(el).on('click', function() {
      $(el).next().focus();
    });
  });
});
