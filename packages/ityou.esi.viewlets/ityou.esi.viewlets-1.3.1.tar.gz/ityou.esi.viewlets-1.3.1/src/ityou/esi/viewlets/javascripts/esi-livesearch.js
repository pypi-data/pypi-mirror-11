$(document).ready(
    function () {

        // --- ANFANG ------
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
        var ls_container = 	$("#livesearch-container");
        /*####erst mal nicht
        ls_container.css("right", 0 - ls_container.width() + $("#liversearch-btn").width() + 20);

        $("#liversearch-btn").click(function(){
            // ist offen -> schließen
            if( ls_container.hasClass("open")  ){
                ls_container
                    .animate({right: 0 - ls_container.width() + $("#liversearch-btn").width() + 20}, 500)
                    .removeClass("open");
                $('#liversearch-btn').removeClass('open')
                $(".livesearch-results").hide()
            }
            // ist zu -> öffnen
            else {
                ls_container.animate({right: 0}, 500).addClass("open")
                $('#liversearch-btn').addClass('open')
                $('#livesearch-input').focus()
            }
		})
        */

        $.get($('#ESI_DATA').data('ityouPortalUrl') + "/++resource++ityou.esi.viewlets.templates/livesearch_contents.html", function(value) {
            contentsTemplate = $.templates(value);
        });
        $.get($('#ESI_DATA').data('ityouPortalUrl') + "/++resource++ityou.esi.viewlets.templates/livesearch_users.html", function(value) {
            usersTemplate = $.templates(value);
        });
	
		$("#livesearch-input").keyup(function(){
			input = $(this);
			delay(function(){
				if(input.val().length > 2) {
					if(input.val() != last_search) {
						last_search = input.val();
						$.getJSON($('#ESI_DATA').data('ityouPortalUrl') + "/@@ajax-content", {
							"action" : "livesearch",
							"search_text": input.val(),
							"max_items": 9
							
						}, function(data){
							$(".livesearch-content-result").detach();
							if(data) {
								$(contentsTemplate.render(data, {
										lower: lowerContent,
										cut: cutContent,
									})).insertAfter(".dropdown-header.contents");
								$(".livesearch-results").show();
							}
						})
						$.getJSON($('#ESI_DATA').data('ityouPortalUrl') + "/@@ajax-users", {
							"action" : "query",
							"q": input.val(),
							"limit": 9							
						}, function(data){
							$(".livesearch-user-result").detach();
							if(data) {
								$(usersTemplate.render(data)).insertAfter(".dropdown-header.users");
								$(".livesearch-results").show();
							}
						})
					}
				}
				else{
					$(".livesearch-results").hide();
				}
			}, 400);
		}).keydown(function(e) {
            var code = e.keyCode || e.which;
            // ESC
            if (code == 27) {
				ls_container
                    .animate({right: 0 - ls_container.width() + $("#liversearch-btn").width() + 20}, 500)
                    .removeClass("open");
                $(".livesearch-results").hide()
                $('#liversearch-btn').removeClass('open')
            } else {
                //console.info(code)
            }
        })
		
		$("#advanced-content-search a").click(function(event){
			event.preventDefault();
			location.href = $('#ESI_DATA').data('ityouPortalUrl') + "/@@search?SearchableText=" + $("#livesearch-input").val() + "*"; 
		})
		
		
		
		$(document).on('click', function(e) {
	    	var inputClicked = $(e.target).attr('id') == 'livesearch-input';
			var resultListClicked = $(e.target).parents('.livesearch-results').length > 0 || $(e.target).hasClass('livesearch-results');
			
			if(inputClicked == false && resultListClicked == false) {
				$('.livesearch-results').hide();
			} else if(inputClicked == true) {
				if($('#livesearch-input').val().length  > 2) {
					$('.livesearch-results').show();
				}
			}
	    });

        // ---- EDNE ----
});
