var lesson_order = 0;

function nextLesson()
{
    console.log(lesson_order);
    //$('#video_'+lesson_order).hide();
    lesson_order += 1;
    console.log(lesson_order);
    //$('#video_'+lesson_order).show();
}

function getData()
{
    $.ajax({
      url: 'get_course_data/',
      type: "GET",
      success: function(response) {
        var lessons = response.lessons;
        for (var i = 0; i < lessons.length; i++)
        {
            var lesson = lessons[i];
            $("body").append("<div id='video_"+lesson.order+" class='video'></div>");
            
            $("#video_"+lesson.order).tubeplayer({
                autoPlay: true,
                width: 600, // the width of the player
                height: 450, // the height of the player
                allowFullScreen: "true", // true by default, allow user to go full screen
                initialVideo: lesson.video_id, // the video that is loaded into the player
                preferredQuality: "default",// preferred quality: default, small, medium, large, hd720
                onPlay: function(id){}, // after the play method is called
                onPause: function(){}, // after the pause method is called
                onPlayerEnded: function(){nextLesson();}, // after the player is stopped
                onSeek: function(time){}, // after the video has been seeked to a defined point
                onMute: function(){}, // after the player is muted
                onUnMute: function(){} // after the player is unmuted
            });
        }
      }
    });
}	

$(function() {
    getData()
    nextLesson();

});