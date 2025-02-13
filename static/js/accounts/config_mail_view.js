// Configuração JS View
    function ajax_send_message()
    {
        $('#send_message_btn').prop("disabled", true);
        $.ajax( 'send_private_message', {
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                'email': $('#email').val(),
                'title': $('#title').val(),
                'message': $('#message').val()
            },
            type: 'post',
            success: function(result) {
                // success code execution here
               if (result.status == 'success')
               {
                    window.location = ""
               }
               else
               {
                    print_error(result.message);
               }

            },
            error: function(xhr,status,error) {
                // error code here
            },
            complete: function(xhr,status) {
                // completion code here
                $('#send_message_btn').prop("disabled", false);
            }
        });
    }

    function ajax_view_message(message_id)
    {
        $('#view_'+message_id+'_btn').prop("disabled", true);
        $.ajax( 'view_private_message', {
            data: {
               'csrfmiddlewaretoken': '{{ csrf_token }}',
               'message_id': message_id
            },
            type: 'post',
            success: function(result) {
               // success code execution here
               $('#ajax_modal').html(result);
               $('#private_message_modal').modal();
            },
            error: function(xhr,status,error) {
               // error code here
            },
            complete: function(xhr,status) {
               // completion code here
               $('#view_'+message_id+'_btn').prop("disabled", false);
            }
        });
    }

    function ajax_delete_message(message_id)
    {
        $('#del'+message_id+'_btn').prop("disabled", true);
        $.ajax( 'delete_private_message', {
            data: {
               'csrfmiddlewaretoken': '{{ csrf_token }}',
               'message_id': message_id
            },
            type: 'post',
            success: function(result) {
               // success code execution here
               window.location = ""
            },
            error: function(xhr,status,error) {
               // error code here
            },
            complete: function(xhr,status) {
               // completion code here
               $('#del'+message_id+'_btn').prop("disabled", false);
            }
        });
    }

/**
 * Prints a error box with the contents of the errors received from the server.
 */
function print_error(message)
{
    $('#error_box').prop("hidden", false); // Display error box.

    // Iterate through the JSON array of arrays and generate an error string.
    var message = "<b>Error(s):</b><hr/>" + "<p>" + message + "</p>";

    // Replace the error string with the contents of the error box.
    $('#error_box').html(message);
}
