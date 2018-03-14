$(document).ready(function() {
  $('form[data-ajax-form]').each(function(i, el) {
    $(el).on('submit', function(e) {
      e.preventDefault();
      $.post({
        url: $(el).attr('action'),
        data: $(el).serialize()
      }).then(function(data) {
        console.log('success: ', data);
      }).catch(function(xhr) {
        console.log('error: ', xhr.responseJSON);
      });
    });
  });
});
