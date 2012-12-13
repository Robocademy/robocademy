function save()
{
	var content = $("form").serialize();
	$.post('save/', content,function(response){
        alert('saving');
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