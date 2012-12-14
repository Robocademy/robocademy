function save()
{
    var data = {};
    data['course_title'] = $('#course_title').val();
    var lesson_order = 0;
    $('form > ol > li').each(function(i) {
        lesson_order += 1;
        data['lesson_'+lesson_order+'_title'] = $(this).find('.lesson_title').val();
        data['lesson_'+lesson_order+'_video_id'] = $(this).find('.lesson_video_id').val();
        var question_order = 0;
        $(this).find('.question_box').each(function(j) {
            question_order += 1;
            data['lesson_'+lesson_order+'_question_'+question_order] = $(this).find('.question').val();
        });
    });
    alert(data);
	//var content = $("form").serialize();
	$.post('save/', data ,function(response){
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