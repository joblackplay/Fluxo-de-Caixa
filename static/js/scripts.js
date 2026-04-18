document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long', day: '2-digit', month: 'long', year: 'numeric'
  });

  function toggleDarkMode() {
    document.body.classList.toggle('dark');
  }

  function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');
  }

  // Carregar dados do Django
  // let chartData = {};
  // const chartScript = document.getElementById('chart-data');
  
  // if (chartScript && chartScript.textContent.trim()) {
  //   try {
  //     chartData = JSON.parse(chartScript.textContent);
  //   } catch (e) {
  //     console.error("Erro ao carregar dados dos gráficos:", e);
  //   }
  // }

  // const dias = chartData.dias || [];
  // const entradasData = chartData.entradas_7dias || [];
  // const saidasData = chartData.saidas_7dias || [];
  // const tiposSaidaLabels = chartData.tipos_saida_labels || [];
  // const tiposSaidaValues = chartData.tipos_saida_values || [];

  // // Gráfico de Barras
  // if (document.getElementById('barChart')) {
  //   new Chart(document.getElementById('barChart'), {
  //     type: 'bar',
  //     data: {
  //       labels: dias,
  //       datasets: [
  //         { label: 'Entradas', data: entradasData, backgroundColor: '#198754', borderRadius: 6 },
  //         { label: 'Saídas',   data: saidasData,   backgroundColor: '#dc3545', borderRadius: 6 }
  //       ]
  //     },
  //     options: {
  //       responsive: true,
  //       maintainAspectRatio: false,
  //       plugins: { legend: { position: 'top' } },
  //       scales: { y: { beginAtZero: true } }
  //     }
  //   });
  // }

  // // Gráfico de Pizza
  // if (document.getElementById('pieChart')) {
  //   new Chart(document.getElementById('pieChart'), {
  //     type: 'doughnut',
  //     data: {
  //       labels: tiposSaidaLabels.length ? tiposSaidaLabels : ['Sem dados'],
  //       datasets: [{
  //         data: tiposSaidaValues.length ? tiposSaidaValues : [100],
  //         backgroundColor: ['#dc3545', '#0d6efd', '#ffc107', '#6f42c1', '#20c997', '#fd7e14']
  //       }]
  //     },
  //     options: {
  //       responsive: true,
  //       maintainAspectRatio: false,
  //       plugins: { legend: { position: 'bottom' } }
  //     }
  //   });
  // }