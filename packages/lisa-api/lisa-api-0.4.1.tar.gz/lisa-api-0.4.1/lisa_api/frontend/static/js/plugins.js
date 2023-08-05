'use strict';

//Make sure jQuery has been loaded before
if (typeof jQuery === "undefined") {
  throw new Error("AdminLTE requires jQuery");
}

$(function() {
    $('.plugin-item-content').matchHeight();
});

$('.button-changelog').click(function(){
     var plugin_name = $(this).attr("href").split(":").pop();
     $('#modal-title').text(plugin_name + ' Changelog');
     $('#ajax').load('/ajax/plugins/changelog/' + plugin_name);
});