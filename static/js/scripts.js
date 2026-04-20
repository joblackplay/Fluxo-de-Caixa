document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long', day: '2-digit', month: 'long', year: 'numeric'
  });

  function toggleDarkMode() {
    document.body.classList.toggle('dark');
  }

  function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');
  }

  document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR', {
    weekday: 'long', day: '2-digit', month: 'long', year: 'numeric'
  });

  