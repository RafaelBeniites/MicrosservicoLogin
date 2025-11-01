document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("formCadastro");
    const toggleSenha = document.querySelector(".toggle-senha");
    const inputSenha = form.querySelector('input[name="senha"]');
    // const btnLogin = document.getElementById("btnLogin"); // REMOVIDO: Não precisamos mais dele

    toggleSenha.addEventListener("click", () => {
        if (inputSenha.type === "password") {
            inputSenha.type = "text";
            toggleSenha.textContent = "🙈";
        } else {
            inputSenha.type = "password";
            toggleSenha.textContent = "👁️";
        }
    });

    function mostrarMensagem(texto, tipo = "erro") {
        const msgBox = document.createElement("div");
        msgBox.className = `mensagem ${tipo}`;
        msgBox.textContent = texto;
        document.body.appendChild(msgBox);

        setTimeout(() => {
            msgBox.classList.add("fadeOut");
            setTimeout(() => msgBox.remove(), 500);
        }, 2500);
    }

    // REMOVIDO: A funcionalidade de clique do botão Login
    // btnLogin.addEventListener("click", () => {
    //   window.location.href = "login.html";
    // });

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const nome = form.nome.value.trim();
        const telefone = form.telefone.value.trim();
        const email = form.email.value.trim();
        const senha = form.senha.value.trim();
        const perfil = form.perfil.value;

        if (!nome || !email || !senha) {
            mostrarMensagem("⚠️ Preencha todos os campos obrigatórios!", "erro");
            return;
        }

        const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!regexEmail.test(email)) {
            mostrarMensagem("❌ E-mail inválido!", "erro");
            return;
        }

        if (senha.length < 6) {
            mostrarMensagem("🔒 A senha deve ter pelo menos 6 caracteres.", "erro");
            return;
        }

        let usuarios = JSON.parse(localStorage.getItem("usuarios")) || [];
        if (usuarios.find((u) => u.email === email)) {
            mostrarMensagem("🚫 Este e-mail já está cadastrado.", "erro");
            return;
        }

        usuarios.push({ nome, telefone, email, senha, perfil });
        localStorage.setItem("usuarios", JSON.stringify(usuarios));

        mostrarMensagem("✅ Conta criada com sucesso! Redirecionando...", "sucesso");

        setTimeout(() => {
            window.location.href = "login.html";
        }, 2500);

        form.reset();
        inputSenha.type = "password";
        toggleSenha.textContent = "👁️";
    });
});