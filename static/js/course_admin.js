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
        var order = $(this).attr('order');
        $(this).parent().find('.answer_choices').append('<span><input name="lesson_'+order+'_answer_{{ x.id }}" type="checkbox" /> <input type="text" name="lesson_'+order+'_answer_choice_" value="" /> <input class="delete_answer_choice" type="button" value="X" /><br/></span>')
    });
    $('.delete_lesson').live('click', function() {
        $(this).parent().parent().remove();
    });
    $('.append_new_lesson').live('click', function() {
        $(this).parent().parent().after($(this).parent().parent().html());
    });
    $('.prepend_new_lesson').live('click', function() {
        $(this).parent().parent().before($(this).parent().parent().html());
    });
    $('.delete_question').live('click', function() {
        $(this).parent().parent().parent().remove();
    });
    $('.delete_answer_choice').live('click', function() {
        $(this).parent().remove();
    });    
    
    $('.append_question').live('click', function() {
        $(this).parent().parent().parent().after($(this).parent().parent().parent().html());
    });
    $('.prepend_question').live('click', function() {
        $(this).parent().parent().parent().before($(this).parent().parent().parent().html());
    });
});