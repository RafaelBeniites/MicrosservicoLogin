// ======== Redireciona para a tela de cadastro ========
document.getElementById("btnCadastro").addEventListener("click", (e) => {
  e.preventDefault();
  window.location.href = "Cadastro.html";
});

// ======== Exibe mensagens bonitas ========
function showMessage(msg, type = "error") {
  const flash = document.getElementById("message");
  flash.textContent = msg;
  flash.className = `flash-message ${type}`;
  
  // animação suave
  flash.classList.add("show");

  setTimeout(() => {
    flash.classList.remove("show");
  }, 4000);
}

// ======== Login ========
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = e.target.email.value.trim();
  const senha = e.target.senha.value.trim();

  try {
    const resposta = await fetch("http://localhost:8080/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, senha }),
    });

    const dados = await resposta.json();

    if (!resposta.ok) {
      showMessage(dados.detail || "Erro no servidor. Tente novamente.", "error");
      return;
    }

    showMessage(`Bem-vindo(a), ${dados.email}!`, "success");
    setTimeout(() => {
      window.location.href = "http://localhost:5173/";
    }, 1500);

  } catch (erro) {
    console.error(erro);
    showMessage("Erro de conexão com o servidor.", "error");
  }
});
