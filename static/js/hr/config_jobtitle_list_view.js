// Configuração JS list view em job title
$(document).on("click", ".showJobSubTitle", function (e) {

  var data_id = $(this).attr("data-id")
  var data_url = $(this).attr("data-url")

  console.log(data_id)
  console.log(data_url)

  $.get(data_url,
    function(data) {
       $(data_id).html(data)
    }
  );
});