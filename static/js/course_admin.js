function save()
{
	var content = $("form").serialize();
	$.post('save/', content,function(response){
        $('#message').text('Saved').show(0).delay(5000).hide(0);        
	});    
}

$(function() {
    $('#save').click(function() {
        save();
    });
    $(document).bind('keydown', 'ctrl+s', function(e) {
        save();
        e.preventDefault();
        return false;
    });
    

});