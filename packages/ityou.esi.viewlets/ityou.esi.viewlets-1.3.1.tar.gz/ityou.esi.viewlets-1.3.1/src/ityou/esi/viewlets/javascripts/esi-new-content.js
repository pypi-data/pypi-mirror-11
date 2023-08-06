$(document).ready(

    // ---- anfang ------------------------
    function () {
        var delay = (function(){
        var timer = 0;
        return function(callback, ms){
            clearTimeout (timer);
		    timer = setTimeout(callback, ms);
		};
    })();

    function lowerContent(value) {
        return value.toLowerCase();
    }

    function cutContent(value, len) {
        if(value.length > len){
            return value.slice(0, len) + " [...]";			
        } else {
            return value;
        }
    }

    last_search = "";

    var nc_container = 	$("#new-content-container");

    nc_container.css("right", 0 - nc_container.width() );

    $("#new-content-btn, #new-content-widget-button").click(function(){
        if( nc_container.hasClass("open")  ){
            nc_container
                .animate({right: 0 - nc_container.width() }, 384, function() {
                	nc_container.hide();
                })
                .removeClass("open")
            $(this).removeClass('fa-minus-circle').addClass('fa-plus-circle ')

        }
        else {
        	nc_container.show();
            nc_container.animate({right: 0}, 384)
                .addClass("open")				
            $(this).removeClass('fa-plus-circle').addClass('fa-minus-circle')
        }
    })
    //nc_container.show()
    
    $(document).on('click', function(e) {
    	var containerClicked = $(e.target).parents('#new-content-container').length > 0 || $(e.target).attr('id') == 'new-content-container';
    	var buttonClicked = $(e.target).find('#new-content-widget-button').length > 0 || $(e.target).find('#new-content-btn').length > 0 || $(e.target).attr('id') == 'new-content-widget-button' || $(e.target).attr('id') == 'new-content-btn'; 
    	
    	
    	if(containerClicked == false && buttonClicked == false) {
    		if(nc_container.hasClass('open')) {
    			$('#new-content-btn, #new-content-widget-button').trigger('click');
    		}
    	}
    });
    

    $('#new-document-box').find('#folder-switcher').find('li').mouseenter(function(){
        if(!($(this).hasClass('fs-active'))){
            $(this).addClass('fs-mouseover');
		}
    });

    $('#new-document-box').find('#folder-switcher').find('li').mouseleave(function(){
        if(!($(this).hasClass('fs-active'))){
            $(this).removeClass('fs-mouseover');
        }
    });
		
    $('#new-document-box').find('.home-folder').hide();
    $('#new-document-box').find('#home-folder-help').hide();

    $('#new-document-box').find('#folder-switcher').find('li').click(function(){
        if($(this).hasClass('fs-mouseover')){
            $(this).removeClass('fs-mouseover');
            $(this).parent().children().each(function(){
	            $(this).toggleClass('fs-active');
            })
            $('#new-document-box').find('.this-folder').toggle();
            $('#new-document-box').toggleClass("home-folder-active");
            $('#new-document-box').find('.home-folder').toggle();
            $('#new-document-help').find('div').toggle();
        }
    })
	}

);
