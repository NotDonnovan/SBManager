$(document).ready(function() {
    $('select').formSelect();
    $('.tooltipped').tooltip();

    $('.dropdown-trigger').dropdown({
    coverTrigger: false,
    hover: true,
    constrainWidth: false,
    });
  });
