var width;
var height;

var lesson_order = 1;
var lessons = {}
var answer_ids = {}
var left_to_go = 0;
var wrong = false;
var responsive_quizzing = true;
var replay_video_automatically = false;
var show_image_on_top_of_question = true;
function askToContinue()
{
    $('#video_'+lesson_order).html('<div style="text-align:center"><p>Good job! Do you want to continue?</p><input type="button" class="continue" value="Continue" /></div>');
}

function nextLesson()
{
    window.location.hash = lesson_order;
    if (lesson_order == lessons.length) {
        $('#video_'+lesson_order).html('Congrats! You finished the course.');
    } else {
        $('.small_video').tubeplayer("stop");
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
    $("#video_"+lesson_order).html('<p class="question_statement">'+lesson.question+'</p><div class="small_video"></div><ul>').css('background', '#FFF').css('text-align', 'left');;
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
            switch (lesson.content_type)
            {
                case "youtube_id":
                    $("#video_"+lesson.order).tubeplayer({
                        width: width, // the width of the player
                        height: height, // the height of the player
                        allowFullScreen: "true", // true by default, allow user to go full screen
                        initialVideo: lesson.content, // the video that is loaded into the player
                        preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
                        onPlayerEnded: function(){setQuestion();},
                        onPlay: function(id){}, // after the play method is called
                        onPause: function(){}, // after the pause method is called
                        onSeek: function(time){}, // after the video has been seeked to a defined point
                        onMute: function(){}, // after the player is muted
                        onUnMute: function(){} // after the player is unmuted
                    });
                    break;
                case "text":
                    $("#video_"+lesson.order).html('<p style="font-size:1.5em">'+lesson.content+'</p>').css('text-align', 'center');
                    $("#video_"+lesson.order).append('<input type="button" value="Next" class="set_question" />');
                    break;       
                case "image":
                    $("#video_"+lesson.order).html('<input type="button" value="Next" class="set_question" />').css('background', 'url('+lesson.content+') no-repeat').css('height', height);    
                    break;                    
            }

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
                if (replay_video_automatically) {
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
                } else {
                    $('.small_video').html('<input type="button" class="rewatch" value="Rewatch video" />');
                }
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
        $(this).parent().parent().html('<div class="new_video"></div>');
        $('.new_video').tubeplayer({
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
        //alert('reanswer');
        setQuestion();
    });   
}	

$(function() {
    width = $(window).width();
    total_height = $(window).outerHeight();
    if (show_image_on_top_of_question) {
        height = $(window).width() / 2;
        
    } else {
        height = total_height;
    }
    
    console.log('width '+ width);
    console.log('height '+ height);
    $('.video').css('width', width);
    $('.video').css('height', height);
    
    getData()
    $(window).on('hashchange',function() {
        var hash = location.hash.substring(1); // strip the leading # symbol
        // now run code based on whatever the value of 'hash' is
        lesson_order = parseInt(hash)
        nextLesson();
    });
    $('.set_question').live('click', function() {
        setQuestion();
    });

});