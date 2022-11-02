$(document).ready(function() {
	
    // Social Media Collapse
	$('#sm-close').click(function(){
		$('.s-media').addClass('sm-collapse');
        $('#sm-open').delay(300).css('left', '0');
	});

    $('#sm-open').click(function(){
        $('#sm-open').css('left', '-60px');
        $('.s-media').removeClass('sm-collapse');
        
    });

});