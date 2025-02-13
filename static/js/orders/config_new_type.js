// Configuração JS new type order
 let total_forms = 0;
    $('#add_more').click(function () {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
            total_forms = $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
    $('#rem_btn').click(function () {
        console.log("Clicou")
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        if(form_idx > 1) {
            $('.empty_topic').last(-1).remove();
            $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) - 1);
        }
    });
            {#console.log(total_forms.val())#}