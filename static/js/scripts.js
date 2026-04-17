  document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long', day: '2-digit', month: 'long', year: 'numeric'
  });

  function toggleDarkMode() {
    document.body.classList.toggle('dark');
  }

  function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');

  }

  const barCtx = document.getElementById('barChart').getContext('2d');
  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
      datasets: [
        {
          label: 'Entradas',
          data: [450, 780, 620, 910, 1250, 680, 920],
          backgroundColor: '#198754',
          borderRadius: 6,
        },
        {
          label: 'Saídas',
          data: [320, 450, 510, 680, 890, 420, 650],
          backgroundColor: '#dc3545',
          borderRadius: 6,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'top' } },
      scales: { y: { beginAtZero: true } }
    }
  });

  // ==================== GRÁFICO DE PIZZA ====================
  const pieCtx = document.getElementById('pieChart').getContext('2d');
  new Chart(pieCtx, {
    type: 'doughnut',
    data: {
      labels: ['Fornecedor', 'Aluguel', 'Salário', 'Marketing', 'Outros'],
      datasets: [{
        data: [35, 25, 20, 12, 8],
        backgroundColor: ['#dc3545', '#0d6efd', '#ffc107', '#6f42c1', '#20c997']
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });
