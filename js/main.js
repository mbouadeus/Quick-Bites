function init() {

  $('.restaurant_item').click(function () {
    var form = $(this).parent();
    form.submit();
  })
}

$(document).ready(init);
