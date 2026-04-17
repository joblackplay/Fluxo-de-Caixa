  // Toggle Sidebar no Mobile
  function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');
  }

  // Fechar sidebar ao clicar fora (melhoria)
  document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth < 768 && !sidebar.contains(e.target) && !e.target.closest('button')) {
      sidebar.classList.remove('show');
    }
  });

  const dialogEntrada = document.getElementById('dialogEntrada');
  const formEntrada = document.getElementById('formEntrada');
  const tbody = document.getElementById('tbodyEntradas');

  function abrirModalEntrada() {
    formEntrada.reset();
    dialogEntrada.showModal();
  }

  function fecharModalEntrada() {
    dialogEntrada.close();
  }

  formEntrada.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('btnSalvar');
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Salvando...`;

    const formData = new FormData(formEntrada);

    try {
      const response = await fetch("{% url 'entrada_create' %}", {
        method: "POST",
        headers: { "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value },
        body: formData
      });

      const data = await response.json();

      if (data.status === 'success') {
        // Adiciona linha dinamicamente
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${data.entrada.data}</td>
          <td>${data.entrada.hora}</td>
          <td><span class="badge bg-success">${data.entrada.tipo_nome}</span></td>
          <td>${data.entrada.descricao}</td>
          <td>${data.entrada.pagamento}</td>
          <td class="text-end fw-bold text-success">R$ ${data.entrada.valor.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
        `;
        tbody.prepend(tr);

        fecharModalEntrada();
        alert("✅ Entrada cadastrada com sucesso!");
      } else {
        alert(data.message || "Erro ao salvar");
      }
    } catch (err) {
      alert("Erro de conexão com o servidor.");
    } finally {
      btn.disabled = false;
      btn.textContent = "Salvar Entrada";
    }
  });