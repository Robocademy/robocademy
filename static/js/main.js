var getStatus = 0;
var countdown = 0;
var countdowni = 10; 
var lastTestCode = false;
var connection_id = 1;

function showFlashError() {
    alert($('#flash_error').html());
    $('#flash_error').show();
}

function clearCmdOutput() {
    $.ajax({
      url: '/devices/set_cmd_status/',
      data: {status: '', connection_id: connection_id},
      type: "POST",
      success: function(response) {
        console.log('cleared cmd output');
      }
    });
}
   
function uploadArduinoCode() {
    $.ajax({
      url: '/devices/send_code/',
      data: {code: editor.getSession().getValue(), connection_id: connection_id},
      type: "POST",
      success: function(response) {
          clearCmdOutput();
          $('#upload_status').html('Uploading (Takes about ten seconds) <span id="upload_countdown"></span>').show();
          $('#cmd_status').text('').show();
          countdown = 1;
          $('#upload_status').css('font-weight', 'bold');
          getStatus = 1;
      }
    });
}

function uploadExampleCode() {
    $.ajax({
      url: '/devices/send_code/',
      data: {code: example.getSession().getValue(), connection_id: connection_id},
      type: "POST",
      success: function(response) {
          clearCmdOutput();
          $('#upload_status').html('Uploading (Takes about ten seconds) <span id="upload_countdown"></span>').show();
          $('#cmd_status').text('').show();
          countdown = 1;
          $('#upload_status').css('font-weight', 'bold');
          getStatus = 1;
      }
    });
}

function testCode() {
    $.ajax({
      url: '/devices/test_code/',
      data: {code: editor.getSession().getValue()},
      type: "POST",
      success: function(response) {
        if (lastTestCode != response.ready)
        {
            if (response.ready) 
            {
                $('#tutorial_status').html('<p id="congrats">Your code is correct. In ten seconds you should see a red light.</p>');
                uploadArduinoCode();
            } else {
                $('#tutorial_status').html('');
            }
        }
        lastTestCode = response.ready;
      }
    });
}

function saveExample() {
    $.ajax({
      url: '/devices/save_example/',
      data: {code: editor.getSession().getValue(), title: $('#code_title').val(), connection_id: connection_id},
      type: "POST",
      success: function(response) {
        $('#message').text('Example saved').show(0).delay(5000).hide(0);
      }
    });
}

function countDown() {
    if (countdown == 1) {
        $('#upload_countdown').text(counttdowni);
        if (countdowni <= 0) {
            countdown = 0;
            countdowni = 10;
        } else {
            countdowni -= 1;
        }
    }
}

function getSerialMonitor() {
    $.ajax({
      url: '/devices/get_serial_monitor/'+connection_id+'/',
      type: "GET",
      success: function(response) {
        $('#serial_monitor').html(response.replace(/\n\n/g, "<br/>"));
      }
    });
}

function getArduinoCodeStatus() {
    if (getStatus == 1) {
        $.ajax({
          url: '/devices/get_status/'+connection_id+'/',
          type: "GET",
          success: function(response) {
            console.log(response);
            if (response == 'True') {
              $('#upload_status').text('Done').show(0).delay(5000).hide(0);
              $('#cmd_status').hide();
              $('#upload_status').css('font-weight', 'bold');
              getStatus = 0;
              countdown = 0;
              countdowni = 10;
            }
          }
        });
        $.ajax({
          url: '/devices/get_cmd_status/'+connection_id+'/',
          type: "GET",
          success: function(response) {
            console.log(response);
            $('#cmd_status').html(response.replace(/\n/g, "<br/>"));
          }
        });
    }
}

function resetArduino()
{
    var code = '\n// basic libraries you need\n#include "Charliplexing.h"\n#include "Arduino.h"\n\nvoid setup()                    // run once, when the sketch starts\n{\n  LedSign::Init(); // initialize LedSign\n}\n\n\nvoid loop()                     // this runs over and over, it\'s the main code area\n{\n  delay(1);\n}\n';
    $.ajax({
      url: '/devices/send_code/',
      data: {code: code, connection_id: connection_id},
      type: "POST",
      success: function(response) {
          
      }
    });
}

function uploadArduinoTurnLightOn()
{
    var code = '\n// basic libraries you need\n#include "Charliplexing.h"\n#include "Arduino.h"\n\nvoid setup()                    // run once, when the sketch starts\n{\n  LedSign::Init(); // initialize LedSign\n}\n\nvoid turn_light_on()\n{\n  LedSign::Set(7, 1, 1);\n  \n}\n\nvoid loop()                     // this runs over and over, it\'s the main code area\n{\n  turn_light_on();\n}\n'
    $.ajax({
      url: '/devices/send_code/',
      data: {code: code, connection_id: connection_id},
      type: "POST",
      success: function(response) {
          
      }
    });
}
var dropdown_html = '';
var dropdown_json = '';
function createDropdowns()
{
    $.ajax({
        url: '/get_dropdown_tree/',
        type: "GET",
        success: function(response) {
            dropdown_json = response;
            dropdown_html = 'Device: <select id="device">';
            for (var i = 0; i < dropdown_json.length; i++)
            {
                var device = dropdown_json[i][0];
                
                dropdown_html += '<option>' + device + '</option>';
                
            }
            var configurations = dropdown_json[0][1];
            dropdown_html += '</select> Configuration: <select id="configuration">';
            for (var i = 0; i < configurations.length; i++)
            {
                var configuration = configurations[i].name;
                var stream = configurations[i].stream;
                console.log(JSON.stringify(configurations[i]));
                dropdown_html += '<option stream="' + stream + '">' + configuration + '</option>';
                
            }
            dropdown_html += '</select>';
            $('#main_selectors').html(dropdown_html);
        }
    });
}

function createLessonsForm()
{
    $.ajax({
      url: '/devices/get_lessons/1/',
      type: "GET",
      success: function(response) {
        var lessons = response.lessons;
        var html = '<table><tr><th class="small">Lesson</th><th class="big">Instructions</th><th class="small">Command pattern</th><th class="big">Code</th></tr>';
        
        for (var i = 0; i < lessons.length; i++)
        {
            var lesson = lessons[i];
            var order = i + 1;
            html += '<tr>';
            html += '<td class="small">' + order + '. <input type="text" name="'+order+'_name" value="' + lesson.name + '" /></td>';
            html += '<td class="big"><textarea name="' + order + '_summary" class="big">' + lesson.summary + '</textarea></td>';
            var command_pattern = ''
            if (lesson.command_pattern)
            {
                command_pattern = lesson.command_pattern;
            }
            html += '<td class="small"><input type="text" name="'+order+'_command_pattern" value="' + command_pattern + '" /></td>';
            html += '<td class="big"><textarea name="' + order + '_stop_code" class="big lesson_textarea">' + lesson.stop_code + '</textarea></td>';
            html += '</tr>';
        }
        html += '</table>';
        $('#lessons_form').html(html);
      }
    });
}

function changeStream(stream_id)
{
    console.log(stream_id);
    var html = '<iframe src="http://www.operationcloud.tv/embed/' + stream_id + '/400/330/FALSE/true" scrolling="no" frameborder="0" style="border: none; overflow:hidden; width: 400px; height: 330px" allowtransparency="true"></iframe>';
    $('#video').html(html);
}

function updateExamples() 
{
    html = '';
    console.log('about to list examples');
    $.ajax({
      url: '/devices/get_examples/' + connection_id + '/',
      type: "GET",
      success: function(response) {
        html = '<select id="select_example"><option></option>';
        //$('#select_example').html('');
        //var list = document.getElementById("selectList");
        //for(var i in response) {
        //  list.add(new Option(response[i].id, response[i].title));
        //}
        console.log('examples being listed');
        console.log(JSON.stringify(response));
        for (var i = 0; i < response.length; i++)
        {
            var example = response[i];
            html += '<option value="' + example.id +'">' + example.title + '</option>';
        }
        //$.each(response, function(x) {   
        // $('#select_example').append($('<option>', {x.id: x.title}).text(value)); 
        //});
        //$('#select_example').append(html);
        html += '</select>';
        $('#examples_dropdown').html(html);
        console.log($('#examples_dropdown').html());
      }
    });
}

function loadStartCode() 
{
    
    $.ajax({
      url: '/devices/get_start_code/' + connection_id + '/',
      type: "GET",
      success: function(response) {
        editor.getSession().setValue(response);
      }
    });
}

function clearExample()
{
    example.getSession().setValue('');
}

function changeConnection(cid, sid)
{
    connection_id = cid;
    changeStream(sid);
    clearExample
    updateExamples();
    loadStartCode();
}

function setStartCode()
{
    $.ajax({
      url: '/devices/set_start_code/',
      data: {code: editor.getSession().getValue(), connection_id: connection_id},
      type: "POST"
    });    
}

$(function() {
    createDropdowns();
    changeConnection(1, 106);
    //createLessonsForm();
    $('#command_box').keypress(function(event) {
        event.preventDefault();
        console.log('command box change');
        $(this).val($(this).val() + String.fromCharCode(event.which));
        if ($(this).val() == 'turn on light')
        {
            console.log('correct code');
            //uploadArduinoTurnLightOn();
            $('#instructions').html("Good job! Here's the light on.").css('font-size', '2em');
            var p = $('#instructions').position()
            var top = p.top + $('#instructions').height();
            var left = p.left;
            $('#video').css({'left': left, 'top': top});
        }
    });
    //resetArduino();
    //uploadArduinoTurnLightOn();
    setInterval(getArduinoCodeStatus, 1000);
    setInterval(getSerialMonitor, 1000);
    setInterval(countDown, 1000);
    $('#set_start_code').click(function() {
        setStartCode();
    });
    $('.lesson_textarea').live('click', function() {
        //alert('hi');
        $(this).css({'position': 'absolute', 'left': 0, 'top': 0, 'width': '100%', 'height': '100%'});
        $('body').append('<input type="button" value="X" />').css({'position': 'absolute', 'top': 0, 'right': 0});
    });
    //setInterval(testCode, 1000);
    $('#save_example').click(function() {
        saveExample();
    });
    $('#upload_code').live('click', function() {
        uploadArduinoCode();
    });
    $('#upload_example').live('click', function() {
        uploadExampleCode();
    });
    $('#arduino_code').bind('keydown', 'ctrl+u', function(e) {
        uploadArduinoCode();
        e.preventDefault();
        return false;
    });
    $(document).bind('keydown', 'ctrl+u', function(e) {
        uploadArduinoCode();
        e.preventDefault();
        return false;
    });
    $('#select_example').live('change', function() 
    {
        var example_id = $(this).attr('value');
        $.ajax({
          url: '/devices/get_example_code/'+connection_id+'/',
          type: "GET",
          data: {id: example_id},
          success: function(response) {
            
            example.getSession().setValue(response.code);
            uploadExampleCode();
          }
        });
    });
    $('#configuration').live('change', function() 
    {
        var stream_id = $(this).find(':selected').attr('stream');
        console.log('about to get connection_id');
        $.ajax({
          url: '/devices/get_connection_id/'+stream_id+'/',
          type: "GET",
          success: function(response) {
            console.log('getting connection id');
            window.connection_id = parseInt(response);
            console.log(connection_id);
            console.log(window.connection_id);
            if (window.connection_id == 2)
            {
                $('#lolshield').show();
            } else {
                $('#lolshield').hide();
            }
            //changeStream(stream_id);
            //updateExamples();
            changeConnection(window.connection_id, stream_id);
            
          }
        });
    });
    $('#array_generator_table td').click(function() {
        if ($(this).hasClass('on_cell')) {
            $(this).removeClass('on_cell');
            $('#'+$(this).attr('codeid')).remove();
        } else {
            $(this).addClass('on_cell');
            
            $('#code_generator').append('<div id="'+$(this).attr('codeid')+'">  '+$(this).attr('code')+'</div>');
        }
        
    });
    // these below are deactivated
    $('#command_box').bind('keydown', 'ctrl+c/', function(e) {
        e.preventDefault();
        alert('Hey! Copying and pasting is cheating. Type out the code by hand.');
        return false;
    });
    $('#command_box').bind('keydown', 'ctrl+v/', function(e) {
        e.preventDefault();
        alert('Hey! Copying and pasting is cheating. Type out the code by hand.');
        return false;
    });
    $(document).bind('keydown', 'ctrl+c/', function(e) {
        e.preventDefault();
        alert('Hey! Copying and pasting is cheating. Type out the code by hand.');
        return false;
    });
    $(document).bind('keydown', 'ctrl+v/', function(e) {
        e.preventDefault();
        alert('Hey! Copying and pasting is cheating. Type out the code by hand.');
        return false;
    });
});