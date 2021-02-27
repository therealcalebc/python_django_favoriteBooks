
$(document).ready(() => {
	console.log("Hello World, this document is ready!");
	
	/* $('div.ninja-list').hide();
	// $('span.dojo-delete').hide();
	// $('button.ninja-delete').hide();
	$('button.dojo-list-item').addClass('data-list-expand');
	$('button.dojo-list-item').hover(function() {
		$(this).addClass('btn-link');
	}, function() {
		$(this).removeClass('btn-link')
	}); */

	/* $('button.dojo-list-item').click(function(event) {
		event.stopPropagation();
		// console.log('dojo-list-item clicked: ' + $(this).html());
		if($(this).hasClass('data-list-expand')) {
			// $(this).children('span.ninja-count').hide();
			$(this).siblings('div.ninja-list').slideDown();
			// $(this).siblings('span.dojo-delete').show();
			// let delBtn = $(this).siblings('button.dojo-delete');
			// delBtn.removeClass('invisible');
			// delBtn.addClass('visible');
		}
		else{
			// $(this).children('span.ninja-count').show();
			$(this).siblings('div.ninja-list').slideUp();
			// $(this).siblings('span.dojo-delete').hide();
			// let delBtn = $(this).siblings('button.dojo-delete');
			// delBtn.removeClass('visible');
			// delBtn.addClass('invisible');
		}
		$(this).toggleClass('data-list-expand')

	}); */

	/* $('span.dojo-delete').click(function(event) {
		$(this).siblings('form').submit();
	})
	$('span.ninja-delete').click(function(event) {
		$(this).siblings('form').submit();
	}) */

	/* $('form').submit(function(event) {
		console.log(event);
		event.preventDefault();
	}); */

	/* document.getElementById('duplicateUserAlert').addEventListener('closed.bs.alert', () => {
		console.log('duplicateUserAlert closed');
		// $("<form method='POST' action='/alert_closed'><input type='hidden' name='alert' value='False'></form>").appendTo("body").submit();
		window.location.href = "alert_closed";
	}); */
})