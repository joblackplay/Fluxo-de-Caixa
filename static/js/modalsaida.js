const dialogSaida = document.getElementById('dialogSaida');
  const formSaida = document.getElementById('formSaida');
  const tbodySaidas = document.getElementById('tbodySaidas');

  function abrirModalSaida() {
    formSaida.reset();
    dialogSaida.showModal();
  }

  function fecharModalSaida() {
    dialogSaida.close();
  }

  // Envio moderno com Fetch API
  formSaida.addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('btnSalvarSaida');
    btn.disabled = true;
    btn.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Salvando...`;

    const formData = new FormData(formSaida);

    try {
      const response = await fetch("{% url 'saida_create' %}", {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
      });

      const data = await response.json();

      if (data.status === 'success') {
        // Adiciona linha dinamicamente na tabela
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${data.saida.data}</td>
          <td>${data.saida.hora}</td>
          <td><span class="badge bg-danger">${data.saida.tipo_nome}</span></td>
          <td>${data.saida.descricao}</td>
          <td>${data.saida.pagamento}</td>
          <td class="text-end fw-bold text-danger">- R$ ${data.saida.valor.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</td>
        `;
        tbodySaidas.prepend(tr);

        fecharModalSaida();
        alert("✅ Saída cadastrada com sucesso!");
      } else {
        alert(data.message || "Erro ao salvar a saída.");
      }
    } catch (err) {
      alert("Erro de conexão com o servidor.");
    } finally {
      btn.disabled = false;
      btn.textContent = "Salvar Saída";
    }
  });

  // Toggle Sidebar no Mobile
  function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('show');
  }