document.addEventListener("DOMContentLoaded", () => {
    let abaAtiva = "pets"; // Inicializa na aba padrão de Animais
    const tabTitle = document.getElementById("tab-title");
    const tableHeader = document.getElementById("tableHeader");
    const tableBody = document.getElementById("tableBody");
    const openModalBtn = document.getElementById("openModalBtn");
    const crudModal = document.getElementById("crudModal");
    const closeModal = document.querySelector(".close-modal");
    const crudForm = document.getElementById("crudForm");
    const formFields = document.getElementById("formFields");
    const modalTitle = document.getElementById("modalTitle");

    // Configurações das tabelas para montar dinamicamente no Front-end
    const colunas = {
        pets: ["Nome do Pet", "Espécie", "Raça", "Nascimento", "Peso (kg)", "Dono/Cliente", "Ações"],
        clientes: ["Nome Completo", "CPF", "Telefone", "Email", "Endereço", "Ações"],
        servicos: ["Serviço", "Descrição", "Preço", "Duração", "Ações"],
        agendamentos: ["Pet", "Dono", "Data", "Hora", "Serviços Contratados", "Total", "Status", "Ações"]
    };

    // 1. Alternar entre as Abas (Tabs) do menu lateral
    document.querySelectorAll(".nav-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            abaAtiva = btn.getAttribute("data-tab");
            atualizarInterface();
        });
    });

    function atualizarInterface() {
        tabTitle.innerText = `Gestão de ${abaAtiva.charAt(0).toUpperCase() + abaAtiva.slice(1)}`;
        
        // Monta o Cabeçalho da tabela baseado nas colunas declaradas acima
        tableHeader.innerHTML = colunas[abaAtiva].map(col => `<th>${col}</th>`).join("");
        carregarDadosTabela();
    }

    // 2. READ: Buscar registros do Django MySQL via Fetch API
    async function carregarDadosTabela() {
        tableBody.innerHTML = `<tr><td colspan="10" style="text-align:center;">Carregando registros...</td></tr>`;
        try {
            const response = await fetch(`/api/listar/${abaAtiva}/`);
            const dados = await response.json();
            
            if (dados.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="10" style="text-align:center;">Nenhum registro encontrado.</td></tr>`;
                return;
            }

            tableBody.innerHTML = dados.map(item => {
                if (abaAtiva === "pets") {
                    return `<tr>
                        <td><strong>${item.nome_pet}</strong></td>
                        <td>${item.especie}</td>
                        <td>${item.raca}</td>
                        <td>${item.data_nascimento}</td>
                        <td>${item.peso} kg</td>
                        <td><span class="badge-owner">${item.dono}</span></td>
                        <td><button class="btn-delete" data-id="${item.id}"><i class="fas fa-trash"></i></button></td>
                    </tr>`;
                } else if (abaAtiva === "clientes") {
                    return `<tr>
                        <td>${item.nome}</td>
                        <td>${item.cpf}</td>
                        <td>${item.telefone}</td>
                        <td>${item.email}</td>
                        <td>${item.endereco}</td>
                        <td><button class="btn-delete" data-id="${item.id}"><i class="fas fa-trash"></i></button></td>
                    </tr>`;
                } else if (abaAtiva === "servicos") {
                    return `<tr>
                        <td>${item.nome_servico}</td>
                        <td>${item.descricao}</td>
                        <td>R$ ${item.preco.toFixed(2)}</td>
                        <td>${item.duracao} min</td>
                        <td><button class="btn-delete" data-id="${item.id}"><i class="fas fa-trash"></i></button></td>
                    </tr>`;
                } else if (abaAtiva === "agendamentos") {
                    return `<tr>
                        <td>${item.animal}</td>
                        <td>${item.dono}</td>
                        <td>${item.data}</td>
                        <td>${item.hora}</td>
                        <td><small>${item.servicos}</small></td>
                        <td><strong>R$ ${item.valor_total.toFixed(2)}</strong></td>
                        <td><span class="status-pill">${item.status}</span></td>
                        <td><button class="btn-delete" data-id="${item.id}"><i class="fas fa-trash"></i></button></td>
                    </tr>`;
                }
            }).join("");

            // Vincula os eventos de exclusão nos novos botões gerados
            adicionarEventosDeletar();
        } catch (error) {
            tableBody.innerHTML = `<tr><td colspan="10" style="color:red; text-align:center;">Erro ao carregar dados.</td></tr>`;
        }
    }

    // 3. DELETE: Apagar do Banco de dados
    function adicionarEventosDeletar() {
        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", async () => {
                const id = btn.getAttribute("data-id");
                if (confirm(`Tem certeza que deseja remover este item da tabela de ${abaAtiva}?`)) {
                    const response = await fetch(`/api/excluir/${abaAtiva}/${id}/`, { method: "DELETE" });
                    const res = await response.json();
                    alert(res.message);
                    carregarDadosTabela();
                }
            });
        });
    }

    // 4. MODAL DINÂMICO: Montar os formulários específicos de cadastro ao abrir o modal
    openModalBtn.addEventListener("click", async () => {
        modalTitle.innerText = `Cadastrar Novo em ${abaAtiva.toUpperCase()}`;
        formFields.innerHTML = ""; // Limpa campos antigos

        if (abaAtiva === "clientes") {
            formFields.innerHTML = `
                <input type="text" id="nome_completo" placeholder="Nome Completo" required class="custom-input">
                <input type="text" id="cpf_cliente" placeholder="CPF (Apenas números)" maxlength="11" class="custom-input">
                <input type="text" id="telefone_cliente" placeholder="Telefone" required class="custom-input">
                <input type="email" id="email_cliente" placeholder="Email" required class="custom-input">
                <input type="text" id="endereco_cliente" placeholder="Endereço Completo" required class="custom-input">
            `;
        } else if (abaAtiva === "pets") {
            // Busca a lista de clientes existentes para criar o select de Donos de Pets
            const res = await fetch('/api/listar/clientes/');
            const clientes = await res.json();
            const optionsClientes = clientes.map(c => `<option value="${c.id}">${c.nome}</option>`).join("");

            formFields.innerHTML = `
                <input type="text" id="nome_pet" placeholder="Nome do Pet" required class="custom-input">
                <input type="text" id="especie" placeholder="Espécie (ex: Cachorro)" required class="custom-input">
                <input type="text" id="raca" placeholder="Raça" required class="custom-input">
                <label style="font-size:12px; margin-top:5px; display:block;">Data de Nascimento:</label>
                <input type="date" id="data_nascimento" required class="custom-input">
                <input type="number" step="0.01" id="peso" placeholder="Peso (kg)" required class="custom-input">
                <textarea id="observacoes" placeholder="Observações médicas ou alergias" class="custom-input" style="grid-column: span 2;"></textarea>
                <select id="cliente_id" required class="custom-input" style="grid-column: span 2;">
                    <option value="" disabled selected>Selecione o Dono (Cliente)</option>
                    ${optionsClientes || '<option disabled>Cadastre um cliente primeiro!</option>'}
                </select>
            `;
        } else if (abaAtiva === "servicos") {
            formFields.innerHTML = `
                <input type="text" id="nome_servico" placeholder="Nome do Serviço" required class="custom-input">
                <input type="text" id="descricao_servico" placeholder="Breve Descrição" required class="custom-input">
                <input type="number" step="0.01" id="preco_servico" placeholder="Preço Cobrado (R$)" required class="custom-input">
                <input type="number" id="duracao_servico" placeholder="Duração Média (em minutos)" required class="custom-input">
            `;
        } else if (abaAtiva === "agendamentos") {
            formFields.innerHTML = `<p style="grid-column: span 2; color:#666;">Agendamentos devem ser realizados pelos clientes através da página pública de <a href="/agendamentos/" target="_blank">Agendamento</a>.</p>`;
        }

        crudModal.style.display = "flex";
    });

    // 5. CREATE: Enviar o Formulário montado acima via POST JSON para o Django
    crudForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (abaAtiva === "agendamentos") return; // Proteção visual

        const payload = {};
        // Captura o valor de cada input criado dinamicamente dentro da div
        formFields.querySelectorAll("input, select, textarea").forEach(field => {
            payload[field.id] = field.value;
        });

        try {
            const response = await fetch(`/api/cadastrar/${abaAtiva}/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const resultado = await response.json();
            alert(resultado.message);

            if (resultado.status === "sucesso") {
                crudModal.style.display = "none";
                crudForm.reset();
                carregarDadosTabela();
            }
        } catch (error) {
            alert("Ocorreu um erro ao tentar salvar no banco MySQL.");
        }
    });

    // Controles visuais de fechar o Modal
    closeModal.addEventListener("click", () => crudModal.style.display = "none");
    window.addEventListener("click", (e) => { if (e.target === crudModal) crudModal.style.display = "none"; });

    // Execução Inicial automática ao carregar a tela
    atualizarInterface();
});