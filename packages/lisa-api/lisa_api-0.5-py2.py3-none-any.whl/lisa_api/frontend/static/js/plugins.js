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
    $('#ajax').load('/ajax/plugins/changelog/' + plugin_name, function( response, status, xhr ) {
        if ( status == "error" ) {
            $( "#ajax" ).html( response );
        }
    });
});

$('.button-readme').click(function(){
    var plugin_name = $(this).attr("href").split(":").pop();
    $('#modal-title').text(plugin_name + ' Readme');
    $('#ajax').load('/ajax/plugins/readme/' + plugin_name, function( response, status, xhr ) {
        if ( status == "error" ) {
            $( "#ajax" ).html( response );
        }
    });
});

$('.button-uninstall').click(function(){
    var timeout_reload = 5;
    var plugin_name = $(this).attr("href").split(":").pop();
    $(this).html($(this).attr('data-progresstext') + ' <img src="' + $(this).attr('data-image') +'" />');
    $.ajax({
        url: '/api/v1/core/plugins/' + plugin_name + '/',
        type: 'POST',
        headers: {'X-HTTP-Method-Override': 'DELETE'},

        success : function(){
            setTimeout(function(){
                location.reload();
            }, timeout_reload * 1000);
        }
    });
});

$('.button-install').click(function(){
    var timeout_reload = 5;
    var action_name = $(this).attr("href").split(":")[0];
    var plugin_name = $(this).attr("href").split(":")[1];
    var version = $(this).attr("href").split(":")[2];

    var type = 'POST';
    var url = '/api/v1/core/plugins/';

    console.log(action_name);
    console.log(plugin_name);
    console.log(version);
    if(action_name == '#upgrade') {
        type = 'PUT';
        url = '/api/v1/core/plugins/' + plugin_name + '/';
    }

    $(this).html($(this).attr('data-progresstext') + ' <img src="' + $(this).attr('data-image') +'" />');
    $.ajax({
        url: url,
        data: {
            'name': plugin_name,
            'version': version
        },
        type: type,

        success : function(){
            setTimeout(function(){
                location.reload();
            }, timeout_reload * 1000);
        }
    });
});

$(document).on("hidden.bs.modal", function (e) {
    $(e.target).removeData("bs.modal").find("#ajax").empty();
});

$('.plugins-filter .search-wrapper input').on('keyup',function(e){
    var input=this;
    var value=this.value,items=$('.plugin-item'),title,desc,author,keywords,value;
    items.css('display','none').each(function(i,item){
        item=$(item);
        value=input.value.toLowerCase();
        title=item.find('h4 a').text().toLowerCase();
        desc=item.find('.plugin-item-content').text().toLowerCase();
        author=item.find('.plugin-item-info').text().toLowerCase();
        keywords=item.find('.plugin-item-keywords').text().toLowerCase();
        if(title.match(value)||keywords.match(value)||desc.match(value)||author.match(value)){
            item.css('display','block');
        }
        else{
            item.css('display','none');
        }
    });
});