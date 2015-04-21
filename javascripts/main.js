'use strict';

function change_lang(obj){
  var val = obj.options[obj.selectedIndex].value;
  var loc = window.location;
  var path = '/S2A';
  if(val === 'ja') path += "/ja";

  console.log(val);
  console.log(path);
  window.location = loc.protocol + '//' + loc.host + path + '/index.html';
}

$(document).ready(function(){
  $('.bxslider').bxSlider({
    captions: true
  });
});

