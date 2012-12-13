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
    $('.add_answer_choice').live('click', function() {
        $(this).parent().find('.answer_choices').append('<input name="lesson_dd_answer_{{ x.id }}" type="checkbox" checked/> <input type="text" name="lesson__answer_choice_" value="" /><br/>')
    });

});