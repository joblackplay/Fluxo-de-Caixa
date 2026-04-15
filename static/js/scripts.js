 document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR', {
      weekday: 'long', day: '2-digit', month: 'long', year: 'numeric'
    });

    // Dark Mode
    function toggleDarkMode() {
      document.body.classList.toggle('dark');
      localStorage.setItem('darkMode', document.body.classList.contains('dark'));
    }
    if (localStorage.getItem('darkMode') === 'true') {
      document.body.classList.add('dark');
      document.getElementById('darkModeToggle').checked = true;
    }

    // Salvar movimentação
    function salvarMovimentacao() {
      const tipo = document.querySelector('input[name="tipo"]:checked').value;
      const descricao = document.getElementById('descricao').value.trim();
      const valorStr = document.getElementById('valor').value;
      const hora = document.getElementById('hora').value || new Date().toLocaleTimeString('pt-BR', {hour:'2-digit', minute:'2-digit'});
      const pagamento = document.getElementById('pagamento').value;

      if (!descricao || !valorStr) {
        alert("Preencha a descrição e o valor!");
        return;
      }

      const valor = parseFloat(valorStr).toLocaleString('pt-BR', {minimumFractionDigits: 2});

      const tbody = document.querySelector("#tabelaMovimentacoes tbody");
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${hora}</td>
        <td>${descricao} <small class="text-muted">(${pagamento})</small></td>
        <td><span class="badge ${tipo === 'entrada' ? 'bg-success' : 'bg-danger'}">${tipo === 'entrada' ? 'Entrada' : 'Saída'}</span></td>
        <td class="text-end fw-semibold ${tipo === 'entrada' ? 'text-success' : 'text-danger'}">R$ ${valor}</td>
      `;
      tbody.prepend(row);


      // Fecha o modal
      //const modal = bootstrap.Modal.getInstance(document.getElementById('movimentacaoModal'));
      //if (modal) modal.hide();
      const modalElement = document.getElementById('movimentacaoModal');
      const modal = bootstrap.Modal.getInstance(modalElement);
      if (modal) {
        modal.hide();
      }
      
      document.getElementById('formMovimentacao').reset();
      alert("✅ Movimentação salva com sucesso!");
    }

    // Hora automática ao abrir modal
    document.getElementById('movimentacaoModal').addEventListener('show.bs.modal', () => {
      document.getElementById('hora').value = new Date().toLocaleTimeString('pt-BR', {hour: '2-digit', minute: '2-digit'});
    });