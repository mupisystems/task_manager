// Configuração JS risk datail

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
var ctx = document.getElementById("myChart").getContext('2d');
var myChart = new Chart(ctx, {
type: 'bar',
data: {
labels: ["Abertos", "Reabertos", "Resolvido", "Encerrado", "Duplicado"],
datasets: [{
label: '{{ object.count_tickets  }} Tickets Ativos',
data: [{% for number in object.count_tickets_in_all_status %} {{ number }}, {% endfor %}],
backgroundColor: [
'rgba(255, 99, 132, 0.2)',
'rgba(54, 162, 235, 0.2)',
{#'rgba(255, 206, 86, 0.2)',#}
{#'rgba(75, 192, 192, 0.2)',#}
{#'rgba(153, 102, 255, 0.2)',#}
{#'rgba(255, 159, 64, 0.2)'#}
],
borderColor: [
{#'rgba(255,99,132,1)',#}
'rgba(54, 162, 235, 1)',
{#'rgba(255, 206, 86, 1)',#}
{#'rgba(75, 192, 192, 1)',#}
{#'rgba(153, 102, 255, 1)',#}
'rgba(255, 159, 64, 1)'
],
borderWidth: 1
}]
},
options: {
scales: {
yAxes: [{
ticks: {
beginAtZero: true
}
}]
}
}
});