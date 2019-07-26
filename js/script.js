
function init() {
  api_key = 'AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno'
  url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key

  fetch(url, {method: 'POST'}).then((res) => {
    res = res.json()

    let lat;
    let lng;
    res = Promise.resolve(res)
    res.then((value) => {
      lat = value['location']['lat']
      lng = value['location']['lng']
      // window.location.href = '/lat=' + lat + '&lng=' + lng

      var form = $('<form action="/" method="post">' +
        '<input type="hidden" name="lat" value="' + lat + '" />' +
        '<input type="hidden" name="lng" value="' + lng + '" />' +
        '</form>');
      $('body').append(form);
      form.submit();
    })

  })
}

$(document).ready(init);
