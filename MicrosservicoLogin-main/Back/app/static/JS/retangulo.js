// ==============================
//  Controle do Retângulo Lateral
// ==============================

const btnToggle = document.getElementById('btnToggle');
const retangulo = document.getElementById('retangulo');

// Alterna a exibição do retângulo ao clicar no botão
btnToggle.addEventListener('click', (e) => {
  e.stopPropagation(); // Evita que o clique feche o retângulo
  if (retangulo.style.display === 'none') {
    retangulo.style.display = 'block';
  } else {
    retangulo.style.display = 'none';
  }
});

// Fecha o retângulo ao clicar fora dele
document.addEventListener('click', (e) => {
  if (!retangulo.contains(e.target) && e.target !== btnToggle) {
    retangulo.style.display = 'none';
  }
});