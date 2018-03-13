$(document).ready(function() {
  function createInputField(el, type, autoclose) {
    $(el).addClass('input-field');
    var name = el.dataset.name,
      label = el.dataset.label;

    var closeTag = autoclose ? ' />' : '></' + type + '>';
    var html = '<' + type + ' name="' + name + '"' + closeTag + '<label class="input-field-label">' + label + '</label>';
    $(el).html(html);

    $(el).find('label').on('click', function() {
      $(el).find(type).focus();
    });

    $(el).find(type).on('blur', function() {
      if (this.value.trim() === '') {
        $(this).removeClass('has-value');
      } else {
        $(this).addClass('has-value');
      }
    });
  }

  $('[data-input-field]').each(function(i, el) {
    createInputField(el, 'input', true);
  });

  $('[data-big-input-field]').each(function(i, el) {
    createInputField(el, 'textarea', false);
  });
});
