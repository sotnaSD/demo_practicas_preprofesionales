var ctx = document.getElementById("bar-chart");
var datos = JSON.parse("{{ datos }}");
var nombres = [];
var valores = [];
var colores = [
  "#3b5998",
  "#E1306C",
  "#0099cc",
  "#c4302b",
  "#db4a39",
  "#ffe600",
  "#a9c6d5",
];
console.log(datos)
datos.forEach(function (elemento) {
  nombres.push(elemento.nombre);
  valores.push(elemento.valor);
});
// console.log(valores1.nombre())
var myBarChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: nombres,
    datasets: [
      {
        label: "Numero de datos",
        backgroundColor: colores,
        data: valores,
      },
    ],
  },
  options: {
    legend: { display: false },
    title: {
      display: true,
      text: "Resultado de las diferentes plataformas",
    },
  },
});
