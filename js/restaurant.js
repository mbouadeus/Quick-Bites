function init() {

  var width = window.innerWidth;
  console.log(width);

  if (width > 600) {
    width = width * .8;
  } else {
    width -= 10;
  }

  $('#header').prepend('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d386950.6511603643!2d-73.70231446529533!3d40.738882125234106!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c24fa5d33f083b%3A0xc80b8f06e177fe62!2sNueva+York!5e0!3m2!1ses-419!2sus!4v1445032011908" width="' + width + '" height="450" frameborder="0" style="margin-left: 10%" allowfullscreen></iframe>')
}

$(document).ready(init);
