 // Configuração JS Modal
 /**
     * Dynamic UI Code.
     *  To give our application a dynamic feel, the following jQuery code will be
     *  used to perform various UI changes.
     */
     $(document).ready(function(){
        $('#private_message_modal').on('hidden.bs.modal', function (e) {
            $('#private_message_modal').html('');
            $('#clost_btn').prop("disabled", false);
        });
    });

    function close_private_message()
    {
        $('#clost_btn').prop("disabled", true);
        $('#private_message_modal').modal('hide');
    }