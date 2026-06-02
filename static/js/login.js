document.addEventListener("DOMContentLoaded", () => {
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('main-container');
    
    const msgDiv = document.getElementById('mensagem');

    // ==================== ANIMAÇÃO DE DESLIZAR AS TELAS ====================
    // Mantemos isso intacto para o efeito visual continuar funcionando perfeitamente!
    if (signUpButton && signInButton) {
        signUpButton.addEventListener('click', () => {
            container.classList.add("right-panel-active");
        });

        signInButton.addEventListener('click', () => {
            container.classList.remove("right-panel-active");
        });
    }

    // ==================== TRATAMENTO VISUAL DE MENSAGENS ====================
    // Função utilitária caso você queira disparar algum alerta via JS futuramente
    function exibirMensagem(texto, tipo) {
        if (msgDiv) {
            msgDiv.innerText = texto;
            msgDiv.style.backgroundColor = tipo === 'sucesso' ? '#2ecc71' : '#e74c3c';
            msgDiv.style.display = "block";
            setTimeout(() => { msgDiv.style.display = "none"; }, 3000);
        }
    }
});