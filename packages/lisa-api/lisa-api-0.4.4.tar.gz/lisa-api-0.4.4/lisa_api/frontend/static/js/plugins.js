'use strict';

//Make sure jQuery has been loaded before
if (typeof jQuery === "undefined") {
  throw new Error("AdminLTE requires jQuery");
}

$(function() {
    $('.plugin-item-content').matchHeight();
     $.ajaxSetup({
        headers: {
            'X-CSRFToken': $.cookie('csrftoken')
        }
    });
});

$('.button-changelog').click(function(){
     var plugin_name = $(this).attr("href").split(":").pop();
     $('#modal-title').text(plugin_name + ' Changelog');
     $('#ajax').load('/ajax/plugins/changelog/' + plugin_name);
});

$('.button-readme').click(function(){
     var plugin_name = $(this).attr("href").split(":").pop();
     $('#modal-title').text(plugin_name + ' Readme');
     $('#ajax').load('/ajax/plugins/readme/' + plugin_name);
});

$('.button-uninstall').click(function(){
     var plugin_name = $(this).attr("href").split(":").pop();
     $.ajax({
         url: '/api/v1/core/plugins/' + plugin_name + '/',
         type: 'POST',
         headers: {'X-HTTP-Method-Override': 'DELETE'},

         success : function(){
             setTimeout(function(){
                 location.reload();
             }, 2000);
         }
    });
});

$('.button-install').click(function(){
     var plugin_name = $(this).attr("href").split(":").pop();
     $.ajax({
         url: '/api/v1/core/plugins/',
         data: {
             'name': plugin_name
         },
         type: 'POST',

         success : function(){
             setTimeout(function(){
                 location.reload();
             }, 2000);
         }
    });
});