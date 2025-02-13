//Configuração JS list view em follow up
function btnonclick(pk) {
     var modal = document.getElementById("myModal"+pk);
    modal.style.display = "block";
    modal.requestFullscreen()
}

function spanonclick(pk) {
     var modal = document.getElementById("myModal"+pk);
  modal.style.display = "none";
  document.exitFullscreen();
}