var width;
var height;

var lesson_order = 1;
var lessons = {}
var answer_ids = {}
var left_to_go = 0;
var wrong = false;
var responsive_quizzing = false;

function askToContinue()
{
    $('#video_'+lesson_order).html('<div style="text-align:center"><p>Good job! Do you want to continue?</p><input type="button" class="continue" value="Continue" /></div>');
}

function nextLesson()
{
    if (lesson_order == lessons.length) {
        $('#video_'+lesson_order).html('Congrats! You finished the course.');
    } else {
        $('.small_video').tubeplayer("stop")
        $('.answer_checkbox').remove();
        $('#video_'+lesson_order).hide();
        lesson_order += 1;
        //alert('#video_'+lesson_order)
        $('#video_'+lesson_order).show();
        $('#video_'+lesson_order).tubeplayer("play");
    }
}

function setQuestion()
{
    wrong = false;
    lesson = lessons[lesson_order - 1];
    answer_ids = lesson.answer_ids;
    //alert(JSON.stringify(lesson))
    $("#video_"+lesson_order).html('<p class="question_statement">'+lesson.question+'</p><div class="small_video"></div><ul>');
    for (var i = 0; i < lesson.answer_choices.length; i++)
    {
        var answer = lesson.answer_choices[i];
        $("#video_"+lesson_order).append('<li><input type="checkbox" value="'+answer.id+'" class="checkbox_answer" /> '+answer.value+'</li>');
    }
    left_to_go = answer_ids.length;
    if (responsive_quizzing) {
        $("#video_"+lesson_order).append('</ul><p><span class="n_to_go">'+left_to_go+'</span> to go</p>');
    } else {
        $("#video_"+lesson_order).append('<input type="button" class="sumbit" value="Sumbit" />');
    }
}

function getData()
{
    $.ajax({
      url: 'get_course_data/',
      type: "GET",
      success: function(response) {
        lessons = response.lessons;
        for (var i = 0; i < lessons.length; i++)
        {
            var lesson = lessons[i];
            $("body").append("<div id='video_"+lesson.order+"' class='video'></div>");
            
            $("#video_"+lesson.order).tubeplayer({
                width: width, // the width of the player
                height: height, // the height of the player
                allowFullScreen: "true", // true by default, allow user to go full screen
                initialVideo: lesson.video_id, // the video that is loaded into the player
                preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
                onPlayerEnded: function(){setQuestion();},
                onPlay: function(id){}, // after the play method is called
                onPause: function(){}, // after the pause method is called
                onSeek: function(time){}, // after the video has been seeked to a defined point
                onMute: function(){}, // after the player is muted
                onUnMute: function(){} // after the player is unmuted
            });
            if (lesson.order != 1)
            {
                $("#video_"+lesson.order).hide();
            }
        }
        //alert($('body').html());
      }
    });
    $('.checkbox_answer').live('click', function() {
        console.log(answer_ids);
        console.log(parseInt($(this).val()));
        console.log(jQuery.inArray(parseInt($(this).val()), answer_ids));
        if (jQuery.inArray(parseInt($(this).val()), answer_ids) < 0)
        {
            //alert('wrong');
            lesson = lessons[lesson_order - 1];
            //alert(lesson.video_id);
            
            if (responsive_quizzing) {
                $(this).parent().addClass('wrong_checkbox');
                $('.small_video').tubeplayer({
                    autoPlay: true,
                    width: 150, // the width of the player
                    height: 113, // the height of the player
                    allowFullScreen: "true", // true by default, allow user to go full screen
                    initialVideo: lesson.video_id, // the video that is loaded into the player
                    preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
                    onPlayerEnded: function(){},
                    onPlay: function(id){}, // after the play method is called
                    onPause: function(){}, // after the pause method is called
                    onSeek: function(time){}, // after the video has been seeked to a defined point
                    onMute: function(){}, // after the player is muted
                    onUnMute: function(){} // after the player is unmuted
                });  
                $(this).parent().prepend('<strong>Wrong:</strong>');
                $(this).remove(); 
            } else {
                wrong == true;
            }            
        } else {
            //alert('correct');
            left_to_go -= 1;
            if (responsive_quizzing) {
                $('.n_to_go').text(left_to_go);
                $(this).parent().addClass('correct_checkbox');
                $(this).parent().prepend('<strong>Correct:</strong>');
                $(this).remove();
                if (left_to_go == 0) {
                    askToContinue();
                }   
            }
     
        }
    });
    $('.continue').live('click', function() {
        nextLesson();
    });
    $('.sumbit').live('click', function() {
        if (wrong || left_to_go != 0) {
            $('#video_'+lesson_order).html('<div style="text-align:center"><p>Your answer is wrong?</p><input type="button" class="reanswer" value="Reanswer question" /><input type="button" class="rewatch" value="Rewatch video" /></div>');

        } else {
            askToContinue();
        }
    });
    $('.rewatch').live('click', function() {
        lesson = lessons[lesson_order - 1];
        //alert($(this).parent().parent().attr('id'));
        //alert(lesson.video_id);
        $(this).parent().parent().html('');
        $(this).parent().parent().tubeplayer({
            width: width, // the width of the player
            height: height, // the height of the player
            allowFullScreen: "true", // true by default, allow user to go full screen
            initialVideo: lesson.video_id, // the video that is loaded into the player
            preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
            onPlayerEnded: function(){setQuestion();},
            onPlay: function(id){}, // after the play method is called
            onPause: function(){}, // after the pause method is called
            onSeek: function(time){}, // after the video has been seeked to a defined point
            onMute: function(){}, // after the player is muted
            onUnMute: function(){} // after the player is unmuted
        });
    });
    $('.reanswer').live('click', function() {
    });   
}	

$(function() {
    width = $(window).width();
    height = $(window).height();
    getData()
    
    

});