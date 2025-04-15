const chartContainer = document.getElementById("chart-data");

const incomes = JSON.parse(chartContainer.dataset.incomes);
const expenses = JSON.parse(chartContainer.dataset.expenses);

var ingresosEgresosOptions = {
    series: [{
        name: 'Ingresos',
        data: incomes
    }, {
        name: 'Egresos',
        data: expenses
    }],
    chart: {
        type: 'area',
        height: 250,
        toolbar: {
            show: false
        }
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth',
        width: 2
    },
    colors: ['#4f46e5', '#ef4444'],
    fill: {
        type: 'gradient',
        gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.2,
            stops: [0, 90, 100]
        }
    },
    xaxis: {
        categories: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
    },
    tooltip: {
        y: {
            formatter: function (val) {
                return "$" + val.toLocaleString();
            }
        }
    }
};

var ingresosEgresosChart = new ApexCharts(document.querySelector("#ingresos-egresos-chart"), ingresosEgresosOptions);
ingresosEgresosChart.render();


  document.addEventListener('DOMContentLoaded', function () {
    const chartContainer = document.getElementById('payment-chart');
    const labels = JSON.parse(chartContainer.dataset.labels);
    const values = JSON.parse(chartContainer.dataset.values);

    const options = {
      chart: {
        type: 'pie',
        height: 300,
      },
      labels: labels,
      series: values,
      colors: ['#4f46e5', '#FBBF24'], // verde para transferencia, amarillo para efectivo
      legend: {
        position: 'bottom',
      },
      responsive: [{
        breakpoint: 480,
        options: {
          chart: {
            width: 300
          },
          legend: {
            position: 'bottom'
          }
        }
      }]
    };

    const chart = new ApexCharts(document.querySelector("#payment-methods-chart"), options);
    chart.render();
  });
  



  const balanceElement = document.getElementById('balance');
  const balanceValue = parseFloat(balanceElement.getAttribute('data-balance'));
  const amountInput = document.getElementById('amount');
  const submitButton = document.getElementById('submit-button');
  const errorMsg = document.getElementById('amount-error');

  amountInput.addEventListener('input', function () {
    const amountValue = parseFloat(amountInput.value);
  
    if (amountValue > balanceValue) {
      submitButton.disabled = true;
      errorMsg.classList.remove('hidden');
  
      amountInput.classList.remove('focus:ring-green-500', 'focus:border-green-500');
      amountInput.classList.add('focus:ring-red-500', 'focus:border-red-500');
    } else {
      submitButton.disabled = false;
      errorMsg.classList.add('hidden');
  
      amountInput.classList.remove('focus:ring-red-500', 'focus:border-red-500');
      amountInput.classList.add('focus:ring-green-500', 'focus:border-green-500');
    }
  });
  