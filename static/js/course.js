var lesson_order = 1;
var lessons = {}
var answer_ids = {}
function nextLesson()
{
    $('.answer_checkbox').remove();
    $('#video_'+lesson_order).hide();
    lesson_order += 1;
    //alert('#video_'+lesson_order)
    $('#video_'+lesson_order).show();
    
}

function setQuestion()
{
    lesson = lessons[lesson_order - 1];
    answer_ids = lesson.answer_ids;
    //alert(JSON.stringify(lesson))
    $("#video_"+lesson_order).html('<p class="question_statement">'+lesson.question+'</p><div style="font-size:1.25em">');
    for (var i = 0; i < lesson.answer_choices.length; i++)
    {
        var answer = lesson.answer_choices[i];
        $("#video_"+lesson_order).append('<input type="checkbox" value="'+answer.id+'" class="checkbox_answer" /> '+answer.value+'<br/>');
    }
    $("#video_"+lesson_order).append('</div>');
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
                width: 600, // the width of the player
                height: 450, // the height of the player
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
        console.log(jQuery.inArray($(this).value(), answer_ids));
        if (!(jQuery.inArray($(this).value(), answer_ids)))
        {
            lesson = lessons[lesson_order - 1];
            $("#video_"+lesson_order).tubeplayer({
                autoPlay: true,
                width: 600, // the width of the player
                height: 450, // the height of the player
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
        } else {
            
        }
    });
}	

$(function() {
    getData()
    
    

});